import os
import psycopg2
from psycopg2.extras import RealDictCursor

DATABASE_URL = (
    f"postgresql://{os.getenv('POSTGRES_USER', 'postgres')}"
    f":{os.getenv('POSTGRES_PASSWORD', 'postgres')}"
    f"@{os.getenv('POSTGRES_HOST', 'localhost')}"
    f":{os.getenv('POSTGRES_PORT', '5432')}"
    f"/{os.getenv('POSTGRES_DB', 'clinic')}"
)


def get_connection():
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS patients (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(100) NOT NULL,
                    age INTEGER NOT NULL,
                    gender VARCHAR(10) NOT NULL,
                    phone VARCHAR(20),
                    created_at TIMESTAMP DEFAULT NOW()
                )
            """)
        conn.commit()
    finally:
        conn.close()
