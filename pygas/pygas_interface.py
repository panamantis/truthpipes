import os,sys
import web3 #pip install web3
from web3 import Web3, HTTPProvider, IPCProvider
from web3.middleware import geth_poa_middleware


#0v1# JC Nov  8, 2019  Expect 4.9.2


print ("Using version: "+str(web3.__version__))



def get_web3(node_name='',verbose=False):

    if node_name=='robsten_3':
        web3_api = Web3(HTTPProvider("https://ropsten.infura.io/v3/5a2597b2866f40d3b704b8ab2cc234b8"))
        # https://mainnet.infura.io/v3/5a2597b2866f40d3b704b8ab2cc234b8
    elif node_name=='mainnet':
        web3_api = Web3(HTTPProvider("https://mainnet.infura.io/v3/5a2597b2866f40d3b704b8ab2cc234b8"))
    else:
        print ("Connecting to blockchain at: "+str(SERVER_ENDPOINT_GLOBAL))
        web3_api = Web3(HTTPProvider(SERVER_ENDPOINT_GLOBAL))

    if verbose:
        print ("Connected.")
    return web3_api


def test_gas_spend():
    web3_api=get_web3(node_name='robsten_3')
    return

if __name__=='__main__':
    branches=['test_gas_spend']

    for b in branches:
        globals()[b]()
        
        
        