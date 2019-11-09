import os
import re
from flask import Flask, render_template, request, jsonify
from pusher import Pusher
import json

from profanityfilter import ProfanityFilter #pip install profanityfilter #https://github.com/areebbeigh/profanityfilter


#0v1# JC Nov  9, 2019


pf = ProfanityFilter()


# create flask app
app = Flask(__name__)

# configure pusher object
pusher = Pusher(
    app_id='893453',
    key='7b7eba95325c46e4012a',
    secret='db4ad3419ecac13d7abf',
    cluster='us2',
    ssl=True
)

LOCAL_DIR=os.path.join(os.path.dirname(__file__), ".")
storage_filename=LOCAL_DIR+"/storage1.tsv"

def censor_phrase(phrase):
    global pf
    return pf.censor(phrase)

def remove_private_info(phrase):
    #scrub email
    phrase=re.sub(r'[\w\.-]+@[\w\.-]+(\.[\w]+)+','',phrase) #no email
    phrase=re.sub(r'[\w\.-]+@[\w\.-]+(\.[\w]+)+','',phrase) #no email
    
    #scrub hex
    phrase=re.sub(r'([0-9A-Fx]){30,100}','',phrase,flags=re.I)
    
    if not phrase:
        phrase=''

    return phrase

def filter_displayed(phrase):
    if len(re.split(r' ',phrase))<3:
        print (".. skipping short feedback: "+str(phrase))
        phrase=''
    phrase=censor_phrase(phrase)
    
    #Remove email address and wallets
    phrase=remove_private_info(phrase)
    
    return phrase

def dict2storage(the_dict):
    global storage_filename
    ffp=open(storage_filename,'a',encoding='utf-8')
    ffp.write(json.dumps(the_dict))
    ffp.write("\n")
    ffp.flush()
    ffp.close()
    return

def load_dicts():
    global storage_filename
    the_dicts=[]
    ffp=open(storage_filename,'r',encoding='utf-8')
    id=-1
    for liner in ffp.readlines():
        id+=1
        dd=json.loads(liner.strip())
        dd['id']=str(id)
        dd['completed']=0

#        dd['value']=censor_phrase(dd['comment'])
        dd['value']=filter_displayed(dd['comment'])
        
        if dd['value'] and dd['value'] is not None:
            the_dicts+=[dd]
    ffp.close()
#    print (">> RETURNING: "+str(the_dicts))
    return the_dicts

# index route, shows index.html view
@app.route('/')
def index():
    ## Initial render
    dds=load_dicts()
    print ("Preloaded: "+str(dds))

    return render_template('index.html',init_data=dds) #<option value="{{ record.comment }}">{{ record.comment }}</option>

# endpoint for storing todo item
@app.route('/add-todo', methods = ['POST'])
def addTodo():
    #JC# data = json.loads(str(request.data)) # load JSON data from request
    data=json.loads(request.get_data().decode('utf8')) #Not data as bytes
    private_contact=data.pop('value2','')
    pusher.trigger('todo', 'item-added', data) # trigger `item-added` event on `todo` channel

    #print ("Should have added: "+str(data))
    #Should have added: {'completed': 0, 'id': 'item-1573074396448', 'value': 'me'}
    dd={}
    dd['comment']=data['value']
#    dd['contact']=private_contact
    dict2storage(dd)
    
    return jsonify(data)

# endpoint for deleting todo item
@app.route('/remove-todo/<item_id>')
def removeTodo(item_id):
    data = {'id': item_id }
    pusher.trigger('todo', 'item-removed', data)
    return jsonify(data)

# endpoint for updating todo item
@app.route('/update-todo/<item_id>', methods = ['POST'])
def updateTodo(item_id):
    data1=json.loads(request.get_data().decode('utf8')) #Not data as bytes
    data = {
      'id': item_id,
      'completed': data1.get('completed', 0)
    }
    pusher.trigger('todo', 'item-updated', data)
    return jsonify(data)

# run Flask app in debug mode
app.run(debug=True)