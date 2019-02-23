# EdgeToll
A Blockchain-based Toll Collection System for Heterogeneous Public Edge Platforms

A research work to be published

# The file architecture
Inside EdgeToll folder, there are 2 folder:


SmartContract (used smart contract development tool named truffle)

edgeBlockChain (used django for proxy server)


# To start

## Publishing Contract
if you want to publish the contract in local:
1. go to SmartContract
2. Open Ganache client
3.

```shell
$ truffle compile
$ truffle migrate --reset
```  
So the address of contract can be found at Ganache, and you can get abi code at builds PC.json


## Set Up server

1. open a terminal and go to edgeBlockChain in EdgeToll
2. runserver
  ```sh
  $ python manage.py runserver
  ```
  
# API of existing system

All methods should be used as Post Request

Register URL : "http://127.0.0.1:7545/regist/"
for edge device to register in server
this url will response a gas fee of open paymentchannel.
parameter: 
- 'address' : the blockchain ethereum address of edge (string in python)


Send Check URL : "http://127.0.0.1:7545/sendCheck/"
for user to post cheque to proxy
this url will response a cost of publish transactions if withdraw_pole = True
parameter:
- 'senderAddress' :  user address
- 'recipientAddress' = proxy address 
- 'valueTransferred' = the value of cheque
- 'v' = the information of signed signature
- 'r' = the information of signed signature
- 's' = the information of signed signature
- 'edgeAddress' = the selected edge address
- 'withdraw_pole' = whether to withdraw, can only be True or False (bool)

Select Edge URL:  "http://127.0.0.1:7545/selectEdge/"
for user to select a target edge, 
this url will response a target edge ssid.
parameter:
- 'edgesWiFi': available edges of user (ssid of WiFi)








 
