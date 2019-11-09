import re


class Ethereum_Model(object):
    def __init__(self,web3=''):
        self.web3=web3
        return
    
    def _load_filename(self,filename):
        fp=open(filename)
        content=fp.read()
        fp.close()
        return content

    def get_contract(self,contractAddress,abi='',abi_filename=''):
        ## Optional bytecode=
        if abi_filename:
            abi=self._load_filename(abi_filename)
        contract=self.web3.eth.contract(contractAddress,abi=abi)
        return contract
    
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
    
    
    ## FUNCTIONS
    #Contract.get_function_by_name(name)
    #https://web3py.readthedocs.io/en/latest/contracts.html#web3.contract.ContractFunction.call
    
