from sklearn.metrics.pairwise import cosine_similarity, euclidean_distances
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
from config import config

def predictContractWinner(corpus, ids, threshold=0.3, similarityType='cos'):
  # number of documents for comparation
  n = len(ids)

  # fit corpus
  matrix = TfidfVectorizer().fit_transform(corpus)
  if (config['debug']):
    print('  fit done')

  # calculate similarity
  similarityFn = cosine_similarity if similarityType == 'cos' else euclidean_distances
  similarityCoeff = 1 if similarityType == 'cos' else -1
  similarities = similarityCoeff * similarityFn(matrix[n:], matrix[:n])
  if (config['debug']):
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
      res.append(unique[sortedCounts[i]])

  return res
