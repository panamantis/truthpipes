import os
import re
import web3
from web3 import Web3
from web3 import Web3, HTTPProvider, IPCProvider
#from web3.middleware import geth_poa_middleware


#0v2# JC Nov  9, 2019  Setup


## Recall set account details
# set ETH_ACCOUNT=
# set ETH_KEY=

print ("Using version (expect 4.9.2): "+str(web3.__version__))


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

def string_to_bytes32(data):
    #Basic for now for string encoding
    if len(data) > 32:
        myBytes32 = data[:32]
    else:
        myBytes32 = data.ljust(32, '0')
    return bytes(myBytes32, 'utf-8')


class Ethereum_Model(object):
    def __init__(self,web3=''):
        self.web3=web3
        self.active_account=''
        self.active_key=''
        return
    
    def _load_filename(self,filename):
        fp=open(filename)
        content=fp.read()
        fp.close()
        return content
    
    def activate_wallet(self,branch=[]):
        if 'system_key' in branch:
            self.active_account=os.environ['ETH_ACCOUNT']
            self.active_key=os.environ['ETH_KEY']
            print ("[info] ethereum account active: "+self.active_account)
        return

    def get_contract(self,contractAddress='',abi='',abi_filename='',meta={}):
        ## Optional bytecode=
        if meta:
            abi_filename=meta['abi_filename']
            contractAddress=meta['contractAddress']

        checksum_address=self.web3.toChecksumAddress(contractAddress)

        if abi_filename:
            abi=self._load_filename(abi_filename)

        Contract=self.web3.eth.contract(checksum_address,abi=abi)
        return Contract
    
    def decode_contract(self,contract_address):
        if not re.search(r'^0x',contract_address):
            zz=40-len(contract_address)
            contract_address='0x'+"0"*zz+contract_address

        #Delegates to eth_getCode RPC Method
        #Returns the bytecode for the given account at the block specified by block_identifier.
        #account may be a hex address or an ENS name

        print ("looking up: "+str(contract_address))
        #code=web3_api.eth.getCode(contract_address)
    
        checksum_address=self.web3.toChecksumAddress(contract_address)
        code=self.web3.eth.getCode(checksum_address)
        #code=BC.web3.eth.getCode(contract_address)
        print ("GOT code: "+str(code))
        print ("GOT code length: "+str(len(code)))
    
        print(''.join([r'\x{:x}'.format(c) for c in code]))
        return code
    
    def gas_price(self):
        print ("See details:  https://ethgasstation.info")

        node_name='robsten_3'
        node_name='mainnet'
        pp=self.web3.eth.gasPrice
        print ("GAS price: "+str(pp))
        pp= Web3.fromWei(pp, 'gwei'),
        print ("GAS wei: "+str(pp))
        return pp
    
    def run_function(self,Contract,params=[],verbose=True):
        if not self.active_account:stopp=no_wallet

        gas_limit=1728712
        gas_price=Web3.toWei('1.2', 'gwei')
        if verbose:
            print ("[eth] gas price for function run: "+str(gas_price))

        # variable, value, type
        #transaction = contract.functions.function_Name(params)
        
        function_name=params[0]
        vvalue=params[1]
        the_type=params[2]
        
        print ("[debug] running function: "+str(function_name)+" setting value: "+str(vvalue))
        
        if the_type=='string':
            vvalue=string_to_bytes32(vvalue) #max length -- encode
        else:
            a=pending_setup
            
        ##1/  Create function object
        #https://github.com/ethereum/web3.py/blob/master/web3/contract.py?
        #function_obj = Contract.functions.setUrl(url) #setUrl object
        the_function=Contract.get_function_by_name(function_name)
        function_obj=the_function(vvalue)
    
        nonce = self.web3.eth.getTransactionCount(self.active_account) #prevents double spend

        transaction_dict=function_obj.buildTransaction(
            {
                'nonce': nonce,
                'from': self.active_account,
                'gas': gas_limit,
                'gasPrice': gas_price
            }
            )
    
        signed=self.web3.eth.account.signTransaction(transaction_dict, self.active_key)
    
        print ("[transaction ready and signed]")
        
        ## send
        print ("Sending transaction...")
        txn_hash = self.web3.eth.sendRawTransaction(signed.rawTransaction) 
        print ("Waiting for transaction to resolve...")
        txn_receipt = self.web3.eth.waitForTransactionReceipt(txn_hash)
        
        print ("Got response: "+str(txn_receipt))
        """AttributeDict({'logs': [], 'contractAddress': None, 'to': '0x8c17eab5d444e80da64823c455ea608f6588c591', 'cumulativeGasUsed': 6165390, 'logsBloom': HexBytes('0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'), 'blockHash': HexBytes('0x5888f2af9d8fba7bcffbbe362d1980ffffb53cb633119ab502d4ac6191cc026a'), 'from': '0x3dd8a3d860fa7ff5b664b96846d3afc3049cff0d', 'status': 1, 'blockNumber': 8903958, 'transactionIndex': 6, 'transactionHash': HexBytes('0x8535fecf36ebcd3756af03d123fd148d7bb453c841717e012e3a33d947cc9946'), 'gasUsed': 65300})"""
    
    
        return

    
    
    ## FUNCTIONS
    #Contract.get_function_by_name(name)
    #https://web3py.readthedocs.io/en/latest/contracts.html#web3.contract.ContractFunction.call
    

        