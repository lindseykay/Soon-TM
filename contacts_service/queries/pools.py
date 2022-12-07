import os
from psycopg_pool import ConnectionPool
import psycopg

conn = psycopg.connect(os.environ["DATABASE_URL"])

reminder_pool = ConnectionPool(conninfo=os.environ["DATABASE_URL2"])
