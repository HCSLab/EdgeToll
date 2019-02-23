from django.test import TestCase

# Create your tests here.

#library
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
from eth_account.messages import defunct_hash_message
import json
import requests
import random

#get contract's address and abi
config = { "address"  : "0xc9C239CDc4d986d8458ebbBe1409ac5d269E3145"}
with open("/Users/a931759898/Desktop/test/1.json") as f:
    config["abi"] = json.load(f)


#implement some function
def sign_transaction(user_address, taker_address, deposit_money):
    message_hash = web3.soliditySha3(['address', 'address', 'uint256'], [user_address, taker_address, deposit_money])
    signed_message = web3.eth.account.signHash(message_hash, private_key=private_key[user_address])
    return (message_hash,signed_message)


def to_32byte_hex(val):
   return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))


#set provider
web3 = Web3(HTTPProvider("http://127.0.0.1:7545"))


#the proxy for trainsiting the money
proxy = web3.eth.accounts[0]


#the sender
user = web3.eth.accounts[1]


#the receiver
edge = web3.eth.accounts[2]

#get the contract
contract_instance = web3.eth.contract(address=config["address"], abi=config['abi'])

private_key = {proxy:'d97979f3ba6851531ec59f2beca5a6956f96e742d3b433484f210fdf26cfbda4', user: 'a08e5a235d53bf82413e7b38e256a7bd1ef684b766d26dc831eb766016090309'}



#how many times of simulation


#edge regist
r = requests.post("http://127.0.0.1:8000/regist/", data={'address': edge})
print('-----------------------------------------------------')
print("The balance for proxy before transaction:", web3.eth.getBalance(proxy))
print("The balance for user before transaction:", web3.eth.getBalance(user))
print("The balance for edge before transaction:", web3.eth.getBalance(edge))



#user build PC itself
contract_instance.functions.openChannel(proxy).transact({'from':user, 'value':10, 'gas':600000})
print('-----------------------------------------------------')


# check the balance
print('The balance for each channel')
print("before transaction:")
print("channel in proxy and edge", contract_instance.functions.getChannelCollateral(proxy, edge).call())
print("channel in user and proxy", contract_instance.functions.getChannelCollateral(user, proxy).call())



#user sign transaction, cost 5 coin
hashmes, signed_message = sign_transaction(user, proxy, 5)


#submit the cheque to proxy
r = requests.post("http://127.0.0.1:8000/sendCheck/", data = {'senderAddress':user, 
'recipientAddress':proxy, 'valueTransferred':5, 'v' : signed_message.v, 'r' : to_32byte_hex(signed_message.r), 's' : to_32byte_hex(signed_message.s)})
print()
print("after transaction:")
print("channel in proxy and edge", contract_instance.functions.getChannelCollateral(proxy, edge).call())
print("channel in user and proxy", contract_instance.functions.getChannelCollateral(user, proxy).call())
print('-----------------------------------------------------')
print("The balance for proxy after transaction:", web3.eth.getBalance(proxy))
print("The balance for user after transaction:", web3.eth.getBalance(user))
print("The balance for edge after transaction:", web3.eth.getBalance(edge))
    
