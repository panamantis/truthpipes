import re
import os
import random
import time
import datetime
import json

from flask import Flask, render_template, request
from flask import jsonify

from tp_rules import Rules_Interface

app = Flask(__name__)

#GLOBAL SETTINGS
LOCAL_DIR=os.path.join(os.path.dirname(__file__), ".")

#0v1# JC Nov  9, 2019  Basic setup


Rules=Rules_Interface()

@app.route('/')
def hello_endpoint():
    global Rules
    dd={}
    dd['hello']='world'
    dd['rules_report']="\n".join(Rules.report())
    return jsonify(dd)
    #return render_template("basic_edit.html",data={}
    
@app.route('/get_rules')
def get_rules_endpoint(*args,**kwargs):
    global Rules
    auto_refresh_on_every_grab=True
    if auto_refresh_on_every_grab:
        Rules=Rules_Interface()

    dd={}
    dd['rules_list']=['a','b']
    dd['rules_list']+=Rules.rules_list()

    dd['rules_report']="\n".join(Rules.report())
    return jsonify(dd)
    #return render_template("basic_edit.html",data={}

        
if __name__ == '__main__':
    app.run(debug=True,port=5000,host='0.0.0.0') #debug=False for auto reload
        
