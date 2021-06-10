#!/usr/bin/env python

import re
import sys
from functools import *
import json


def extract_transactions(log):
    # regexp = re.compile('called \((.* )\)')
    results = re.findall('called \((.* )\)', log)
    return map(lambda a: (a[0].strip(), a[1].strip()), map(lambda m: m.split(','), results))


def extract_transaction_time(transaction, log):
    result = re.search('Submitted transaction\s+ hash=' + transaction+ '.*\n.*Commit new mining work .* elapsed=(\S+)', log)
    time = result.group(1)

    time = time[1:] if time[0] == '"' else time
    time = time[:-1] if time[-1] == '"'  else time
    unit_measure = time[-2:]

    if unit_measure != 'ms':
        time = str(round(float(time[:-2]) / 1000, 4)) + 'ms'
    return float(time[:-2])


def extract_times(log_lottery_file, log_geth_file):
    with open(log_lottery_file, 'r') as f:
        log_lottery = f.read()
    with open(log_geth_file) as f:
        log_geth = f.read()

    transactions = extract_transactions(log_lottery)
    times = map(lambda e: (e[0], e[1], extract_transaction_time(e[1], log_geth)), transactions)
    return times


def average_results(list_results, runs):
    sums = reduce(lambda l1, l2: map(lambda elem: (elem[0][0], elem[0][1], elem[0][2] + elem[1][2]), zip(l1,l2)), list_results)
    averages = map(lambda e: (e[0], e[2] / runs), sums)
    return averages


def generate_block_file(info_file, transactions):
    with open(info_file, "r") as f:
        info = json.load(f)
    block = []
    address = 1000
    block = [{'type': 'constructor', 'called_address': str(address), 'data': info['bytecode']}]
    block.extend([{'type': 'method', 'called_address': str(address), 'data': info['methodsIds'][t[0]]} for t in transactions])
    # print(block)
    with open("generated-block.json", "w") as f:
        json.dump(block, f)


def main():
    if len(sys.argv) != 5:
        sys.stderr.write("Usage:\n python %s contract-run geth-run runs template\n" % sys.argv[0])
        exit(-1)
    runs = int(sys.argv[3])
    if runs < 0:
        sys.stderr.write("Invalid number of runs: %s\n" % sys.argv[3])
        exit(-2)
    else:
        contract_name_p = sys.argv[1]
        geth_run_p = sys.argv[2]
        info_file = sys.argv[4]
        files = [(f"{contract_name_p}{i}.log", f"{geth_run_p}{i}.log") for i in range(1,runs + 1)]
        list_results = map(lambda files: extract_times(files[0], files[1]), files)
        results = list(average_results(list_results, runs))
        print("Length of the result %d" % len(results))
        sequential_time = sum(map(lambda e: e[1], results))
        print("Sequential time cost: %f ms" % (sequential_time))

        with open("transaction-cost.txt", "w") as f:
            for (i, t) in enumerate(results):
                f.write(f"{i+1},{t[0]},{t[1]}\n")

        generate_block_file(info_file, results)


if __name__ == '__main__':
    main()