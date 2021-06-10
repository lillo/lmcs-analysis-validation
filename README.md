# README - A theory of transaction parallelism in blockchains

This repository contains the data and the scripts used for the experimental evaluation described in the paper 
> [M. Bartoletti, L. Galletta and M. Murgia. A theory of transaction parallelism in blockchains](https://arxiv.org/abs/2011.13837), Manuscript under review, 2021.

## Tools used for the experiment
- [Go Ethereum](https://geth.ethereum.org/) v1.10.3-stable-991384a7
- [Truffle](https://www.trufflesuite.com/) v5.3.3
- [Python 3](https://www.python.org/)
- [Commandline dependency builder](https://github.com/lillo/cmd_net_tool)

## Structure of the repository

Here is a high level description of the content of the repository.

```text
.
├── contracts/
|   Source code of the Lottery contract. 
│
├── migrations/
|   Truffle scripts for the migration and deployment of the contract on the blockchain.
│
├── scripts/
|   Scripts used for the generation and analysis of the experiment data   
│
├── experiment-data
|   Data used for the evaluation
│
├── LICENSE
│
├── truffle-config.js
|   Truffle configuration.
│
└── README.md
```

### Scripts 
Here is a high level description of scripts used for the evaluation.

```text
scripts
├── create-account.js
|   Script for the geth console to create further two accounts to play the lottery    
│
├── run-lottery.sh
|   Script bash that creates the required accounts, deploys the contract on the blockchain and plays 70 game of the lottery. It stores the hashes of the sent transactions into a file.
│
├── transactions-lottery.js
|   Truffle script that plays the lottery interacting with the contract on the blockchain.   
│
├── analyze-result.py
|   Script python that extracts the time spent by each transaction from the geth log, that computes the sequential time and that generates the input for cldb tool 
│
└── longest-path.py 
    Script python that given the dependency graph generated by cldb and the execution time of each transaction   computes a parallel schedule as the longest and most expensive path (in terms of time) of the dependency graph. 
```

### Data

Here is a high level description of data generated for the evaluation.

```text
experiment-data
├── geth-run[1-10].log
|   Log generated by geth 
│
├── lottery-run[1-10].log
|   Hashes of transaction generated during the game
│
├── lottery-info.json
|   Template used to generate the block to use as input of cldb
│
├── lottery-generated-block.json
|   The block of transactions used in our evaluation  
│
├── lottery-transaction-cost.txt
|   The cost in term of time of each transaction in lottery-generated-block.json 
|
├── lottery-transaction-graph.txt
|   The dependency graph generated by cldb for transactions in lottery-generated-block.json    
|
└── cldb-time.txt 
    The average time spent by cldb to perform the analysis of transaction in lottery-generated-block.json 
```