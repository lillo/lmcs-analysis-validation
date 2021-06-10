/*
 geth should be run
 ```
 $ geth --dev --http --http.corsdomain="*" --allow-insecure-unlock
 ```
 
 To be run by the geth console
 ```
 $ geth attach /tmp/geth.ipc --exec 'loadScript("create-account.js")'
 ```
*/

user1=personal.newAccount()
user2=personal.newAccount()

eth.sendTransaction({from:eth.coinbase, to:eth.accounts[1], value: web3.toWei(100, "ether")})
eth.sendTransaction({from:eth.coinbase, to:eth.accounts[2], value: web3.toWei(100, "ether")})

personal.unlockAccount(user1)
personal.unlockAccount(user2)

debug.startCPUProfile("/tmp/profile")

