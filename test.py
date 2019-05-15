#!/usr/bin/python

import sys
from db import cur, close
from predictor import predictContractWinner
from success import calculateSuccess
from data_loader import getContractsWithDocumentation
import numpy as np

def main(argv, argc):
  contracts = getContractsWithDocumentation(cur)

  avg = {
    'success': [],
    'precission': [],
    'recall': [],
    'accuracy': [],
  }

  c = 0
  for contractId, *_ in contracts:
    c += 1
    print('Contract', c, '/', len(contracts))
    res = predictContractWinner(cur, contractId, loadSuppliers=True)
    if res:
      print('  candidates:', res['candidates'])
      print('  prediction:', res['prediction'])
      print('  suppliers:', res['suppliers'])
      success = calculateSuccess(res)
      for key, value in success.items():
        avg[key].append(value)
    else:
      print('No result!')

  print('Average of', len(avg['success']), 'contracts')
  for key, value in avg.items():
    print(key, np.average(value))

if __name__ == '__main__':
  main(sys.argv[1:], len(sys.argv) - 1)
  close()
