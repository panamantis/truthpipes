import os,sys
import re
import json

from utils import walk_directory

#sys.path.insert(0,'../pyweb3')
#from truthpipes_service import alg_get_my_pointer_count

#0v1# JC Nov  9, 2019  Base setup

LOCAL_DIR=os.path.join(os.path.dirname(__file__), ".")
RULES_DIR=LOCAL_DIR+"/rules"


class Rules_Interface(object):
    def __init__(self):
        self.rules_records=[]
        self.load_rules()
        return
    
    def load_rules(self):
        for path,filename in walk_directory([LOCAL_DIR]):
            if re.search(r'\.json$',filename):
                fp=open(path)
                c=0
                for liner in fp.readlines():
                    c+=1
                    liner=liner.strip()
                    if liner:
                        print ("FO: "+str(liner))
                        self.rules_records+=[json.loads(liner)]
                print ("<load rules> "+str(filename)+" count: "+str(c))
        return
    
    def load_blockchain_rules(self):
        dd={}
        dd['blockchain_rule1']=''
        dd['my_pointer_count']=alg_get_my_pointer_count()
        print ("[debug] blockchain rule sample dict: "+str(dd))

        self.rules_records+=[dd]
        return
    
    def report(self):
        oa=[]
        oa+=['Rules count: '+str(len(self.rules_records))]
        #for rule in self.rules_records:
        #    oa+=[rule]
        return oa
    
    def rules_list(self):
        the_list=[]
        for rule in self.rules_records:
            the_list+=[rule]
        return the_list
    

def dev1():
    Rules=Rules_Interface()
    return

if __name__=='__main__':
    branches=['dev1']
    for b in branches:
        globals()[b]()
        
        