#!/bin/bash

# to run the miner
# $ geth --dev --http --allow-insecure-unlock

if ["$1" == ""]; then
    echo "Error"
    exit -1
else
  geth attach /tmp/geth.ipc --exec 'loadScript("scripts/create-account.js")' &&
  truffle migrate &&
  (truffle exec scripts/transactions-lottery1.js > $1) 
fi
