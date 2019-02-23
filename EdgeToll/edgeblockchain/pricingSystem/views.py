#libraries
#django, web3
from django.shortcuts import render
from django.http import HttpResponse
from pricingSystem import models
from web3 import Web3, HTTPProvider
from web3.contract import ConciseContract
import json
import requests
import random
import numpy as np

# set up network node, can be changed
web3 = Web3(HTTPProvider("http://127.0.0.1:7545")) #connect to loacl network node 


#the contract address and abi
config = { "address"  : "0xEb38F414F50750f4A32Dd34ea2405f5CE707D695"} #you should change this address into yours deploying contract address
a = [ #the abi of the content of code, should be change to your contracts' abi code
    {
    "constant": True,
    "inputs": [
      {
        "name": "",
        "type": "address"
      },
      {
        "name": "",
        "type": "address"
      }
    ],
    "name": "channels",
    "outputs": [
      {
        "name": "sender",
        "type": "address"
      },
      {
        "name": "recipient",
        "type": "address"
      },
      {
        "name": "collateral",
        "type": "uint256"
      }
    ],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
  },
  {
    "constant": False,
    "inputs": [
      {
        "name": "recipient",
        "type": "address"
      }
    ],
    "name": "openChannel",
    "outputs": [],
    "payable": True,
    "stateMutability": "payable",
    "type": "function"
  },
  {
    "constant": False,
    "inputs": [
      {
        "name": "sender",
        "type": "address"
      },
      {
        "name": "recipient",
        "type": "address"
      },
      {
        "name": "valueTransferred",
        "type": "uint256"
      },
      {
        "name": "v",
        "type": "uint8"
      },
      {
        "name": "r",
        "type": "bytes32"
      },
      {
        "name": "s",
        "type": "bytes32"
      }
    ],
    "name": "closeChannel",
    "outputs": [],
    "payable": False,
    "stateMutability": "nonpayable",
    "type": "function"
  },
  {
    "constant": True,
    "inputs": [
      {
        "name": "sender",
        "type": "address"
      },
      {
        "name": "recipient",
        "type": "address"
      },
      {
        "name": "valueTransferred",
        "type": "uint256"
      },
      {
        "name": "v",
        "type": "uint8"
      },
      {
        "name": "r",
        "type": "bytes32"
      },
      {
        "name": "s",
        "type": "bytes32"
      }
    ],
    "name": "verifySignature",
    "outputs": [
      {
        "name": "",
        "type": "bool"
      }
    ],
    "payable": False,
    "stateMutability": "pure",
    "type": "function"
  },
  {
    "constant": True,
    "inputs": [
      {
        "name": "sender",
        "type": "address"
      },
      {
        "name": "recipient",
        "type": "address"
      }
    ],
    "name": "getChannelCollateral",
    "outputs": [
      {
        "name": "",
        "type": "uint256"
      }
    ],
    "payable": False,
    "stateMutability": "view",
    "type": "function"
  }
]
config['abi'] = a
contract_instance = web3.eth.contract(address=config['address'], abi=config['abi']) #get the contract_instance


#get the accounts information 
#address...
# user = web3.eth.accounts[0]
# proxy = web3.eth.accounts[1]
# edge1 = web3.eth.accounts[2]
# edge2 = web3.eth.accounts[3]
# edge3 = web3.eth.accounts[4]
# private_key = {
#     user: '93eeceaf872686b748acda18ba68acd4c13d2b786203edee237bee8017a79105',
#     proxy:'57730ecf94645a7cbeb381164e8577e1122f6e909f2b46dd839480b8916a4fc2',
#     edge1:'7cad2ea1120dae749e68dfd62af603f423ebc9221fd4ac157b33873528b275d2',
#     edge2:'6cd79303468fe58a83b1c40963331a14b318b6d0497df22e668d319078174921',
#     edge3:'19e5a2a2716310a94704b976755c640bf8a4ec0253c400c080f3bc1849af6d36'
# }

proxy = ''
proxy_private_key = ''




depositToken = 1 #the money deposit every time, can be changed
def index(request):
    """
    receive the address of edge and open payment channel
    input: the address of the edge
    output: open a payment channel for that edge
    """

    if request.method == 'POST':
        #get edge's address
        address = request.POST.get('address')

        #store in database
        models.EdgeInfo.objects.create(address=address, balance=depositToken)

        #build PC for edge
        tx = contract_instance.functions.openChannel(address).buildTransaction({'value': web3.toWei(depositToken, 'ether') ,'nonce': web3.eth.getTransactionCount(proxy), 'gas':600000})
        signed_txn = web3.eth.account.signTransaction(tx, private_key=proxy_private_key)
        a = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        transact_hash = web3.toHex(a)
        gas = web3.eth.waitForTransactionReceipt(transact_hash).gasUsed
        print('On regist....')
        print('The recipiet for tx:', transact_hash)

        #result for register in proxy
        data = {
            'gas': gas,
        }
        data = json.dumps(data,ensure_ascii=False)
        return HttpResponse(data, content_type="application/json")
    


    #refresh the pages
    else:
      user_list = models.EdgeInfo.objects.all()
      return render(request, 'index.html', {'data': user_list})

def sendCheck(request):
    """
    Receiveing the cheque signed by user and then verify the cheque
    if the cheque is legal, send the cheque to edge
    input: the cheque signed by user
    output: send edge a isometric cheque 
    """
    print("it's on send Check..." )
    if request.method == 'POST':
      #get the cheque's information
      senderAddress = request.POST.get('senderAddress')
      recipientAddress = request.POST.get('recipientAddress')
      valueTransferred = int(request.POST.get('valueTransferred'))
      v = int(request.POST.get('v'))
      r = request.POST.get('r')
      s = request.POST.get('s')
      edgeAddress = request.POST.get('usedEdge')
      withdraw_pole = request.POST.get('withdraw')


      #check whether it is a withdraw operation
      if withdraw_pole == 'True':
        withdraw_pole = True
      else:
        withdraw_pole = False
      
      print('The result of check,', contract_instance.functions.verifySignature(senderAddress, recipientAddress, valueTransferred, v, r, s).call())
      print('On sendCheck....')

      if contract_instance.functions.verifySignature(senderAddress, recipientAddress, valueTransferred, v, r, s).call() and withdraw_pole:

        # close the channel between proxy and edge, used for rinkeby
        tx = contract_instance.functions.closeChannel(senderAddress, recipientAddress, valueTransferred, v, r, s).buildTransaction({'nonce': web3.eth.getTransactionCount(recipientAddress), 'gas':600000})
        signed_txn = web3.eth.account.signTransaction(tx, private_key=private_key[recipientAddress])
        a = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        transact_hash = web3.toHex(a)
        gas = web3.eth.waitForTransactionReceipt(transact_hash).gasUsed
        print('The recipiet for tx:', transact_hash)
        print('The result of balance:', contract_instance.functions.getChannelCollateral(senderAddress, recipientAddress).call()) # show the channel balance


        #send to edge
        _, signed_message = sign_transaction(recipientAddress, edgeAddress, valueTransferred, proxy_private_key)
        r = requests.post("http://127.0.0.1:8000/edge/", data = {'senderAddress':recipientAddress, 
        'recipientAddress':edgeAddress, 'valueTransferred': valueTransferred, 'v': signed_message.v, 'r': to_32byte_hex(signed_message.r), 's':to_32byte_hex(signed_message.s), 'withdraw': withdraw_pole})

        #compute the gas cost and return 
        gas2 = json.loads(r.text)['gas']
        data = {
            'gas': gas + gas2,
        }
        data = json.dumps(data,ensure_ascii=False)
        return HttpResponse(data, content_type="application/json")

      else:
        _, signed_message = sign_transaction(recipientAddress, edgeAddress, valueTransferred, proxy_private_key)
        r = requests.post("http://127.0.0.1:8000/edge/", data = {'senderAddress':recipientAddress, 
          'recipientAddress':edgeAddress, 'valueTransferred': valueTransferred, 'v': signed_message.v, 'r': to_32byte_hex(signed_message.r), 's':to_32byte_hex(signed_message.s), 'withdraw': withdraw_pole})
        return HttpResponse('No transaction online!')

    else:
      return HttpResponse("use POST!")


def selectEdge(requests):
  """
  provide user a optimial choice of edge based on requests' information
  the request send by user should contain the available edges' list
  input: available edges' list from user （ the ssid of wifi, e.g.)
  output: optimial edge information  (the ssid of selected wifi)
  """

  if requests.method == 'POST':
    edgesWiFi = requests.POST.getlist('edgesWiFi')

    #selected edge
    edge = edgesWiFi[0] #more select logic can be added into it

    # return json information
    data = {
        'edge': edge,
        'price': min_cost
    }
    data = json.dumps(data,ensure_ascii=False)
    return HttpResponse(data, content_type="application/json")
  else:
    return HttpResponse("it's a select Edge page!")
        



def receiveCheck(request):
    """
    for edge to receive the cheque and close the PC to get eth
    input : cheque signed by proxy
    output : close PC and get eth
    """
    if request.method == 'POST':

      #get information
      senderAddress = request.POST.get('senderAddress')
      recipientAddress = request.POST.get('recipientAddress')
      valueTransferred = int(request.POST.get('valueTransferred'))
      v = int(request.POST.get('v'))
      r = request.POST.get('r')
      s = request.POST.get('s')
      withdraw_pole = request.POST.get('withdraw')

      #check whether the operation is withdraw or not
      if withdraw_pole == 'True':
        withdraw_pole = True
      else:
        withdraw_pole = False
      

      print('On receiveCheck....')
      print('the channel balance of proxy and edge...', contract_instance.functions.verifySignature(senderAddress, recipientAddress, valueTransferred, v, r, s).call())



      if contract_instance.functions.verifySignature(senderAddress, recipientAddress, valueTransferred, v, r, s).call() and withdraw_pole:


        # close PC to get money for rinkeby
        tx = contract_instance.functions.closeChannel(senderAddress, recipientAddress, valueTransferred, v, r, s).buildTransaction({'nonce': web3.eth.getTransactionCount(recipientAddress), 'gas':600000})
        signed_txn = web3.eth.account.signTransaction(tx, private_key=private_key[recipientAddress])
        a = web3.eth.sendRawTransaction(signed_txn.rawTransaction)
        transact_hash = web3.toHex(a)
        gas = web3.eth.waitForTransactionReceipt(transact_hash).gasUsed
        
        print('The recipiet for tx:', transact_hash)
        print('The getChannelCollateral :', contract_instance.functions.getChannelCollateral(senderAddress, recipientAddress).call())
        print(contract_instance.functions.getChannelCollateral(senderAddress, recipientAddress).call())

        #return gas result
        data = {
            'gas': gas,
        }
        data = json.dumps(data,ensure_ascii=False)
        return HttpResponse(data, content_type="application/json")

      else:
        return HttpResponse("Invalid transaction!")
    else:
      return HttpResponse("use Post!")
        


    


def sign_transaction(user_address, taker_address, deposit_money, _privatekey):
    """
    to sign a cheque
    input: signer's address, receiver's address, amount
    output: the hash of the message and the signed message
    """
    message_hash = web3.soliditySha3(['address', 'address', 'uint256'], [user_address, taker_address, deposit_money])
    signed_message = web3.eth.account.signHash(message_hash, private_key=_privatekey)
    return (message_hash,signed_message)


def to_32byte_hex(val):
    """
    for data type conversion
    To invoke the solidity's function correctly
    """
    return Web3.toHex(Web3.toBytes(val).rjust(32, b'\0'))
