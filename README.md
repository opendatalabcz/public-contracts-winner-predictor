# public-contracts-winner-predictor

## About this project
The goal of this project is to predict a winner of a public contract using the contract's documentation.

This project is dependant on both [opendata](https://github.com/opendatalabcz/opendata) and [public-contracts](https://github.com/opendatalabcz/public-contracts) projects.

## Installation
1. Install [PostgreSQL](https://www.postgresql.org/).
2. Install [Python 3.7](https://www.python.org/).
3. Create the opendata DB schema as specified [here](https://github.com/opendatalabcz/opendata/blob/master/docs/install.md).
4. Extend the DB schema with public-contracts specific tables as specified [here](https://github.com/opendatalabcz/public-contracts) and download data.
5. Clone this repository and install dependencies using `pip install -r requirements.txt`.
6. Create config.json (using the [config.json.template](config.json.template) file).

## Configuration

- db
  - psycopg2 connection string as specified [here](http://initd.org/psycopg/docs/module.html)
  - required
- dict & tagger
  - path to MorphoDiTa dict & tagger files which can be downloaded [here](http://ufal.mff.cuni.cz/morphodita/users-manual#czech-morfflex-pdt)
  - required
- debug
  - whether or not to print debug messages
  - default is false
- similarityType
  - whether to use cosine similarity (cos) or euclidean similarity (euc)
  - default is euc
- similarityThreshold
  - similarity value below which documents are ignored
    - e.g. for cosine similarity and threshold = 0.3, if the best fit for a document has similarity of 0.29, it's not accepted.
  - default is -10
  - note that when using euclidean similarity, all values are negative or zero (the best possible value)
- lemmatize
  - whether to lemmatize documents before vectorization
  - default is false

## How to run the app
Using the run.py file:
```bash
# Predict winner of a contract with ID 123
py run.py 123

# Predict winner of a contract with ID 123
# and compare the prediction with actual suppliers
py run.py 123 true
```

## How to test the app:
Using the test.py file:
```bash
# Test all possible contracts
py test.py

# Test all possible contracts
# and store predictions to a JSON file
py test.py export.json
```
