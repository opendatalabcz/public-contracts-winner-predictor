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
- missingLimit
  - maximum accepted ratio of missing candidates data
  - default is 0.0

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

## Experiments
The application has been tested on public contracts of Czech ministries for several configurations using leave-one-out cross-validation. Results can be seen in the following table:

| similarityType | similarityThreshold | lemmatize | missingLimit | contracts amount | success (absolute equality\*) | accuracy |
|-|-|-|-|-|-|-|
| cos | 0.3 | true | 0.0 | 163 | 0.724 | 0.836 |
| cos | 0.9 | true | 0.0 | 163 | 0.736 | 0.862 |
| cos | 0.3 | false | 0.0 | 163 | 0.748 | 0.861 |
| cos | 0.9 | false | 0.0 | 163 | 0.755 | 0.871 |
| euc | -10 | true | 0.0 | 163 | 0.773 | 0.856 |
| euc | -0.9 | false | 0.0 | 163 | 0.773 | 0.867 |
| euc | -1 | false | 0.0 | 163 | 0.804 | 0.878 |
| euc | -10 | false | 0.0 | 163 | 0.804 | 0.881 |
| euc | -10 | false | 0.3 | 272 | 0.691 | 0.873 |
| euc | -10 | false | 0.4 | 350 | 0.706 | 0.881 |
| euc | -10 | false | 0.5 | 472 | 0.758 | 0.907 |

As you can see, best results were obtained using euclidean similarity and threshold of -10. Surprisingly lemmatization had a negative impact on the score.

Even when working with incomplete data (see rows with missingLimit > 0), the accuracy is about 88 %. Also in majority of cases, the success (absolute equality\*) is over 70 %.

\* Absolute equality means that the prediction and actual suppliers must be completely the same. For example when candidates are [1, 2, 3] and suppliers are [1], then the prediction must be exactly [1]. However if the prediction would be [1, 2] (because entities 1 & 2 might be very similar), then it would help only to the accuracy mesaure and not to the success measure.
