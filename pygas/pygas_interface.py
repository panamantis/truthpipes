import os,sys
import web3 #pip install web3


from eth_model import Ethereum_Model
from eth_model import get_web3


#0v1# JC Nov  8, 2019  Expect 4.9.2


print ("Using version: "+str(web3.__version__))


def test_gas_spend():
    web3_api=get_web3(node_name='robsten_3')
    return


def test_get_gas_price():
    web3_api=get_web3(node_name='robsten_3')
    Eth=Ethereum_Model(web3=web3_api)
    
    Eth.gas_price()
    return


if __name__=='__main__':
    branches=['test_gas_spend']
    branches=['test_get_gas_price']

    for b in branches:
        globals()[b]()
        
        
        