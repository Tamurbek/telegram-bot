import os
import time
import psycopg2
from dotenv import load_dotenv

load_dotenv()

PG_HOST = os.getenv("PG_HOST", "db")
PG_DB = os.getenv("PG_DB")
PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_PORT = os.getenv("PG_PORT", 5432)

def wait_for_db(retries=30, delay=2):
    for i in range(retries):
        try:
            conn = psycopg2.connect(
                host=PG_HOST,
                database=PG_DB,
                user=PG_USER,
                password=PG_PASSWORD,
                port=PG_PORT,
                connect_timeout=3
            )
            conn.close()
            print("Postgres tayyor.")
            return True
        except Exception as e:
            print(f"DBga ulanib bo‘lmadi, kutilyapti... ({i+1}/{retries})")
            time.sleep(delay)
    raise RuntimeError("Postgresga ulanib bo‘lmadi.")

if __name__ == "__main__":
    wait_for_db()