import os
import time
import psycopg2
from psycopg2 import OperationalError

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_PORT = os.getenv("DB_PORT")
DB_HOST = os.getenv('DB_HOST', 'db')

def wait_for_db():
    print("⏳ Waiting for PostgreSQL...")

    while True:
        try:
            conn = psycopg2.connect(
                dbname=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                host=DB_HOST,
                port=DB_PORT,
            )
            conn.close()
            print("PostgreSQL is ready!")
            break
        except OperationalError as e:
            print(f"PostgreSQL not ready ({e}), retrying in 2s...")
            time.sleep(2)


if __name__ == "__main__":
    wait_for_db()