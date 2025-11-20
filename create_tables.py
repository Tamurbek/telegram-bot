import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

conn = psycopg2.connect(
    host=os.getenv("PG_HOST", "db"),
    database=os.getenv("PG_DB"),
    user=os.getenv("PG_USER"),
    password=os.getenv("PG_PASSWORD"),
    port=os.getenv("PG_PORT", 5432)
)

cur = conn.cursor()
cur.execute("""
CREATE TABLE IF NOT EXISTS videos (
    id SERIAL PRIMARY KEY,
    file_id TEXT NOT NULL,
    caption TEXT
);
""")
conn.commit()
cur.close()
conn.close()
print("Tables created / already exist.")