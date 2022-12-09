import os
import psycopg

kwargs = {
    "autocommit": True
}
conn = psycopg.connect(conninfo= os.environ["DATABASE_URL"], **kwargs)
