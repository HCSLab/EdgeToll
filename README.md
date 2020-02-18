# EdgeToll
A Blockchain-based Toll Collection System for Heterogeneous Public Edge Platforms

[Click for papers](https://mypage.cuhk.edu.cn/academics/caiwei/paper/XiaoFGC2019.pdf)

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

1. open a terminal and go to edgeblockchain in EdgeToll
2. runserver
  ```sh
  $ python manage.py runserver
  ```
  
# API of existing system

All methods should be used as Post Request and listed parameters should be provided as data.

#### Register URL : "http://127.0.0.1:7545/regist/"
for edge device to register in server, after posting request, the proxy will open a paymentchannel for the provided address
parameter: 
- 'address' : the blockchain ethereum address of edge (string in python)
return: gas fee of registeration 



####  Send Check URL : "http://127.0.0.1:7545/sendCheck/"
for user to post cheque to proxy
parameter:
- 'senderAddress' :  user address
- 'recipientAddress' = proxy address 
- 'valueTransferred' = the value of cheque
- 'v' = the information of signed signature
- 'r' = the information of signed signature
- 's' = the information of signed signature
- 'edgeAddress' = the selected edge address
- 'withdraw' = whether to withdraw, can only be True or False (bool)
return: gas cost of publish trasactions when 'withdraw' = True

#### Select Edge URL:  "http://127.0.0.1:7545/selectEdge/"
for user to select a target edge, 
parameter:
- 'edgesWiFi': available edges of user (ssid of WiFi)
return: a target edge's ssid for connection









 
