import psycopg2 as pg
from config import config

conn = pg.connect(config['db'])
cur = conn.cursor()

def close():
  cur.close()
  conn.close()
