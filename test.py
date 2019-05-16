#!/usr/bin/python

import sys
from db import cur, close
from predictor import predictContractWinner
from score import calculateScore
from data_loader import getContractsWithDocumentation
import numpy as np
import json

def main(argv, argc):
  contracts = getContractsWithDocumentation(cur)

  avg = {
    'success': [],
    'precision': [],
    'recall': [],
    'accuracy': [],
  }
  results = []

  c = 0
  for contractId, *_ in contracts:
    c += 1
    print('Contract', c, '/', len(contracts))
    res = predictContractWinner(cur, contractId, loadSuppliers=True)
    if res:
      results.append(res)
      print('  candidates:', res['candidates'])
      print('  prediction:', res['prediction'])
      print('  suppliers:', res['suppliers'])
      score = calculateScore(res)
      for key, value in score.items():
        avg[key].append(value)
    else:
      print('  No result!')

  print('Average of', len(avg['success']), 'contracts')
  for key, value in avg.items():
    print(key, np.average(value))

  if argc > 0:
    with open(argv[0], 'w') as file:
      json.dump(results, file)

if __name__ == '__main__':
  main(sys.argv[1:], len(sys.argv) - 1)
  close()
