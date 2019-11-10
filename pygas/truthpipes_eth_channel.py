import os

from eth_model import Ethereum_Model
from eth_model import get_web3

#0v1# JC Nov  9, 2019  

LOCAL_DIR=os.path.join(os.path.dirname(__file__), ".")




def load_truthpipes_contract_meta(branch=['ResilientEndpoint']):
    meta={}
    
    if 'PolicyRegistry' in branch:
        meta['contractAddress']='0x605a4fbd92f5930513f7950abd93e83c78ff2dde' #PolicyRegistry
        meta['abi_filename']=LOCAL_DIR+'/smart_contracts/policy_registry_1.abi'

    if 'ResilientEndpoint' in branch:
        meta['contractAddress']='0x8c17eab5d444e80da64823c455ea608f6588c591' #ResilientEndpoint
        meta['abi_filename']=LOCAL_DIR+'/smart_contracts/resilient_endpoint_1.abi'
    return meta


def alg_get_truthpipes_url(verbose=True):
    contract_meta=load_truthpipes_contract_meta()
    web3_api=get_web3(node_name='mainnet')
    
    Eth=Ethereum_Model(web3=web3_api)
    Contract=Eth.get_contract(meta=contract_meta)
    
    response=Contract.functions.url().call()
    if not 'http' in response.lower():
        response="http://"+response
    if verbose:
        print ("truthpipes url: "+str(response))
    return response


def alg_get_minted_rules():
    rules_texts=[]
    #Main account for now
    Eth,Contract=common_load_PolicyRegistry()
    
    b=['just_one_rule_dev']
    
    if 'just_one_rule_dev' in b:
        params=[(Eth.active_account,'address')] #wiki string/url
        response_list=Eth.run_function(Contract,'getPolicy',params=params,is_call=True)
        rules_texts+=[response_list[2]] # 0 name, 1 url, 2 wiki
     
    return rules_texts

def alg_mint_rule_text(the_text):
    #** for now to single account!!
    if len(the_text)>300:
        print ("**warning, clipping text to mint.")
        the_text=the_text[:300]

    Eth,Contract=common_load_PolicyRegistry()
    b=['just_one_rule_dev']
    if 'just_one_rule_dev' in b:
        #** see create in test_mint_comment()
        params=[]
        params+=[('sample_name_1','string')] #name string
        params+=[('sample_url_1','string')] #image string/url
        params+=[('sample_wiki_1',the_text)] #wiki string/url
        txn_receipt=Eth.run_function(Contract,'createPolicy',params=params)
    return

def common_load_PolicyRegistry():
    contract_meta=load_truthpipes_contract_meta(branch=['PolicyRegistry'])
    web3_api=get_web3(node_name='mainnet')
    Eth=Ethereum_Model(web3=web3_api)
    Contract=Eth.get_contract(meta=contract_meta)
    Eth.activate_wallet(branch=['system_key'])
    return Eth,Contract


def test_get_url():
    response=alg_get_truthpipes_url()
    print ("Test get urL: "+str(response))
    return


def test_set_url():
    ## Load std
    url='truthpipes.com:5000'
    print ("Setting ResilientEndpoint on ethereum mainnet to: "+url)

    contract_meta=load_truthpipes_contract_meta(branch=['ResilientEndpoint'])
    web3_api=get_web3(node_name='mainnet')
    Eth=Ethereum_Model(web3=web3_api)
    Contract=Eth.get_contract(meta=contract_meta)
    
    Eth.activate_wallet(branch=['system_key'])
    
    Eth.run_function(Contract,'setUrl',params=[(url,'string')])

    return


def test_mint_comment():
    comment="https://www.amazon.com/DDT-Death-Dealer-Tactical-Assassin/dp/B00GHZCAUA/ref=sr_1_2?dchild=1&keywords=ddt&qid=1573341131&sr=8-2"

    Eth,Contract=common_load_PolicyRegistry()
    
    params=[]
    b=['create']
    b=['update']
    b=['view']

    if 'create' in b:
        params+=[('sample_name_1','string')] #name string
        params+=[('sample_url_1','string')] #image string/url
        params+=[('sample_wiki_1','string')] #wiki string/url
        Eth.run_function(Contract,'createPolicy',params=params)

    if 'update' in b:

#ok>32bytes        params+=[('sample_name_100000000000000000001','string')] #name string
        params+=[('samp','string')] #name string

        # updatePolicyWiki(string _wiki) public {
        Eth.run_function(Contract,'updatePolicyWiki',params=params)

    if 'view' in b:
        params=[(Eth.active_account,'address')] #wiki string/url
        response_list=Eth.run_function(Contract,'getPolicy',params=params,is_call=True)
        print ("GOT: "+str(response_list))

    return

def test_standalone_get_rules_texts():
    texts=alg_get_minted_rules()
    for rule in texts:
        print ("Got rule text: "+str(rule))
    return


if __name__=='__main__':
    branches=['test_set_url']
    branches=['test_get_url']
    branches=['test_mint_comment']

    branches=['test_standalone_get_rules_texts']

    for b in branches:
        globals()[b]()
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        