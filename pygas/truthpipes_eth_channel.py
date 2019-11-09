import os

from eth_model import Ethereum_Model
from eth_model import get_web3

#0v1# JC Nov  9, 2019  

LOCAL_DIR=os.path.join(os.path.dirname(__file__), ".")




def load_truthpipes_contract_meta(branch=['ResilientEndpoint']):
    meta={}
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
    
    Eth.run_function(Contract,('setUrl',url,'string'))

    return


if __name__=='__main__':
    branches=['test_set_url']
    branches=['test_get_url']

    for b in branches:
        globals()[b]()
        
        
        