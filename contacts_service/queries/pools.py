import os
from psycopg_pool import ConnectionPool

pool = ConnectionPool(conninfo=os.environ["DATABASE_URL"])


reminder_pool = ConnectionPool(conninfo="postgresql://postgres:password@db:5432/reminders")

