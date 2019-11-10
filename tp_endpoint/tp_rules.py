import os,sys
import re
import json

from utils import walk_directory

sys.path.insert(0,'../pygas')
from truthpipes_eth_channel import alg_get_minted_rules

#from truthpipes_service import alg_get_my_pointer_count

#0v1# JC Nov  9, 2019  Base setup

LOCAL_DIR=os.path.join(os.path.dirname(__file__), ".")
RULES_DIR=LOCAL_DIR+"/rules"



class Rules_Interface(object):
    def __init__(self):
        self.rules_records=[]
        self.load_rules()
        return
    
    def load_rules_from_ethereum(self):
        print ("[debug] fetching minted rules for ethereum...")
        rule_texts=alg_get_minted_rules()
        print ("[debug] done fetch")

        for rule_text in rule_texts:
            rule={}
            rule['dummy_minted']=rule_text
            self.rules_records+=[rule]
        return

    def load_rules_from_webui_flatfile(self):
        hardcoded_storage_filename=LOCAL_DIR+"/../idea_tracker/storage1.tsv"
        fp=open(hardcoded_storage_filename,'r',encoding='utf-8')
        for liner in fp.readlines():
            dd=json.loads(liner.strip())
            
            ## Mapping
            rule={}
            rule['dummy']=dd['comment']
            #  {"highlight_amazon":["B07BHNHP9F"]}
            self.rules_records+=[rule]
        fp.close()
        return

    def load_rules_from_dummy(self):
        #  {"ok":"1"}
        #  {"highlight_amazon":["B07BHNHP9F"]}

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
    
    
    def load_rules(self):
        self.load_rules_from_dummy()
        self.load_rules_from_webui_flatfile()
        self.load_rules_from_ethereum()

        ## Auto augment rules
        # -- ie/ pull out all mentioned asins
        aug_rules=[]
        arules={} #list rules
        arules['highlight_amazon']=[]

        for rule in self.rules_records:
            new_rules=auto_rule_augmentation(rule)
            for rule in new_rules:
                #Combine if multiple amazons
                if 'highlight_amazon' in rule:
                    arules['highlight_amazon']+=rule['highlight_amazon'] #list append
                else:
                    aug_rules+=[rule]

        aug_rules+=[arules]
        self.rules_records=aug_rules
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
    

def auto_rule_augmentation(rule):
        #  {"highlight_amazon":["B07BHNHP9F"]}
    ##GIVEN:   {'dummy':'sadfklj ds ds B07BHNHP9F '}
    ##RETURN:  {'highlight_amazon':'B07BHNHP9F'}
    new_rules=[]
    
    new_rules+=[rule] #keep original

    amazon_asins=[]
    for kk in rule:
        content=rule[kk]
        for mention in re.findall(r'\bB[\dA-Z]+',content):
            amazon_asins+=[mention]
            
#D    print ("[debug assins: "+str(amazon_asins))
    if amazon_asins:
        nrule={}
        nrule['highlight_amazon']=amazon_asins
        new_rules+=[nrule]
        
    return new_rules


def test_load_rules():
    Rules=Rules_Interface()
    for rule in Rules.rules_list():
        print ("RUL: "+str(rule))
    return


def dev_rule_augmentation():
    given={'dummy':'sadfklj ds ds B07BHNHP9F '}
    got=auto_rule_augmentation(given)
    expect={'highlight_amazon':'B07BHNHP9F'}
    print ("EXPECTED: "+str(expect))
    print ("GOT: "+str(got))
    return


if __name__=='__main__':
    branches=['dev_rule_augmentation']
    branches=['test_load_rules']
    for b in branches:
        globals()[b]()
        
        
        
        
        
        
        
        
        
