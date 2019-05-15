from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from config import config
from data_loader import getCandidates, getCandidatesData, getDocumentation, getSuppliers
from lemmatizer import lemmatize

def predictContractWinnerFromCorpus(corpus, ids, threshold, similarityType):
  # number of documents for comparation
  n = len(ids)

  # fit corpus
  matrix = TfidfVectorizer().fit_transform(corpus)
  if config.get('debug'):
    print('  fit done')

  # calculate similarity
  similarityFn = cosine_similarity if similarityType == 'cos' else euclidean_distances
  similarityCoeff = 1 if similarityType == 'cos' else -1
  similarities = similarityCoeff * similarityFn(matrix[n:], matrix[:n])
  if config.get('debug'):
    print('  similarity done')

  # for every contract document find the best fit in candidate documents
  predictions = []
  for sim in similarities:
    sortedSim = (-sim).argsort()
    best = sim[sortedSim[0]]
    for i in range(len(sortedSim)):
      val = sim[sortedSim[i]]
      if val != best or val < threshold:
        break

      predictions.append(ids[sortedSim[i]])

  # find candidates with the highest amount of similar documents
  res = []
  unique, counts = np.unique(predictions, return_counts=True)

  if len(counts) != 0:
    sortedCounts = (-counts).argsort()
    best = counts[sortedCounts[0]]
    for i in range(len(sortedCounts)):
      if counts[sortedCounts[i]] != best:
        break
      res.append(int(unique[sortedCounts[i]]))

  return res

def predictContractWinner(cur, contractId, loadSuppliers=False):
  if config.get('debug'):
    print('contract', contractId)

  # load candidates along with the documentation of contracts they won
  candidates = getCandidates(cur, contractId)
  candidatesData = getCandidatesData(cur, candidates, contractId)
  ids = list(map(lambda x: x[0], candidatesData))
  missing = len([x for x in candidates if x not in ids])

  if config.get('debug'):
    print('  missing', missing, '/', len(candidates), '=', float(missing) / float(len(candidates)))

  # check if the amount of missing candidates exceeds the limit
  missingLimit = config.get('missingLimit', 0)
  if missing > missingLimit:
    if config.get('debug'):
      print('  skipping')
    return None

  # initialize corpus
  corpus = []
  shouldLemmatize = config.get('lemmatize', False)

  # add candidates data to the corpus
  d = 0
  for eid, docType, docData in candidatesData:
    corpus.append(lemmatize(docData) if shouldLemmatize else docData)
    d += 1
    if config.get('debug') and d % 25 == 0:
      print('  candidate data', d, '/', len(candidatesData))

  if config.get('debug'):
    print('  candidate data done')

  # add contract data to the corpus
  docs = getDocumentation(cur, contractId)
  for docType, docData in docs:
    corpus.append(lemmatize(docData) if shouldLemmatize else docData)

  if config.get('debug'):
    print('  corpus done')

  # optionally load suppliers for further evaluation
  suppliers = getSuppliers(cur, contractId) if loadSuppliers else None

  # predict winners
  threshold = config.get('similarityThreshold', 0.3)
  similarityType = config.get('similarityType', 'cos')
  prediction = predictContractWinnerFromCorpus(corpus, ids, threshold, similarityType)

  return {
    'contract': contractId,
    'candidates': candidates,
    'suppliers': suppliers,
    'prediction': prediction,
  }
