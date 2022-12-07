import os
from psycopg_pool import ConnectionPool
import psycopg

# pool = ConnectionPool(conninfo=os.environ["DATABASE_URL"])
conn = psycopg.connect(os.environ["DATABASE_URL"])