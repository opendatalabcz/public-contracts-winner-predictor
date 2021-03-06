#!/usr/bin/python

import sys
from db import cur, close
from predictor import predictContractWinner
from score import calculateScore

def main(argv, argc):
  if argc == 0:
    print('Missing contract ID!')
    close()
    sys.exit(1)

  contractId = int(argv[0])
  loadSuppliers = argv[1] == 'true' if argc > 1 else False

  res = predictContractWinner(cur, contractId, loadSuppliers)
  if res:
    print('candidates:', res['candidates'])
    print('prediction:', res['prediction'])

    if loadSuppliers:
      print('suppliers:', res['suppliers'])
      score = calculateScore(res)
      for key, value in score.items():
        print(key, value)
  else:
    print('No result!')

if __name__ == '__main__':
  main(sys.argv[1:], len(sys.argv) - 1)
  close()
