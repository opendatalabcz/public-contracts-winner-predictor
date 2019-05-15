# Load contracts that are linked with documentation
# (documents whose types contain "dokumentace")
# and have candidates and suppliers.
# This is used mainly for testing.
def getContractsWithDocumentation(cur):
  cur.execute('''
    SELECT
      c.contract_id,
      COUNT(DISTINCT d.document_id) AS documents_count,
      COUNT(DISTINCT s.entity_id) AS entities_count,
      COUNT(DISTINCT ca.entity_id) AS candidates_count
    FROM contract c
    JOIN document d ON d.contract_id = c.contract_id
    JOIN supplier s ON s.contract_id = c.contract_id
    JOIN candidate ca ON ca.contract_id = c.contract_id
    WHERE
      d.type ILIKE '%dokumentace%'
      AND d.data IS NOT NULL
    GROUP BY c.contract_id
    HAVING
      COUNT(DISTINCT d.document_id) > 0
      AND COUNT(DISTINCT s.entity_id) > 0
      AND COUNT(DISTINCT ca.entity_id) > 1
  ''')

  return cur.fetchall()

# Load documentation for a specific contract
def getDocumentation(cur, contractId):
  cur.execute('''
    SELECT
      d.type,
      d.data
    FROM document d
    WHERE
      d.type ILIKE '%%dokumentace%%'
      AND d.data IS NOT NULL
      AND d.contract_id = %s
    ORDER BY d.document_id ASC
  ''', (contractId,))

  return cur.fetchall()

# Load candidates for a specific contract
def getCandidates(cur, contractId):
  cur.execute('''
    SELECT ca.entity_id
    FROM candidate ca
    WHERE ca.contract_id = %s
  ''', (contractId,))

  return list(map(lambda x: x[0], cur.fetchall()))

# Load suppliers for a specific contract
def getSuppliers(cur, contractId):
  cur.execute('''
    SELECT s.entity_id
    FROM supplier s
    WHERE s.contract_id = %s
  ''', (contractId,))

  return list(map(lambda x: x[0], cur.fetchall()))

# Load documentation for candidates from other contracts.
# Optionally ignore specific contract to avoid conflicts and overfitting.
def getCandidatesData(cur, candidates, ignoreContractId=-1):
  cur.execute('''
    SELECT
      s.entity_id,
      d.type,
      d.data
    FROM document d
    JOIN contract c ON c.contract_id = d.contract_id
    JOIN supplier s ON
      s.contract_id = c.contract_id
      AND s.entity_id IN %s
    WHERE
      d.type ILIKE '%%dokumentace%%'
      AND d.data IS NOT NULL
      AND d.contract_id != %s
    ORDER BY d.document_id ASC
  ''', (tuple(candidates), ignoreContractId))

  return cur.fetchall()
