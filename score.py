import numpy as np

# Calculate success, precision, recall and accuracy
def calculateScore(res):
  tp = len(np.intersect1d(res['suppliers'], res['prediction']))
  fp = len(np.setdiff1d(res['prediction'], res['suppliers']))
  tn = len(np.setdiff1d(np.setdiff1d(res['candidates'], res['suppliers']), res['prediction']))
  fn = len(np.setdiff1d(res['suppliers'], res['prediction']))

  return {
    'success': 1 if np.array_equal(res['suppliers'], res['prediction']) else 0,
    'precision': float(tp) / (float(tp) + float(fp)) if tp + fp != 0 else 0,
    'recall': float(tp) / (float(tp) + float(fn)) if tp + fn != 0 else 0,
    'accuracy': (float(tp) + float(tn)) / float(len(res['candidates'])),
  }
