import os
from contextlib import contextmanager

import psycopg
from dotenv import load_dotenv

load_dotenv()

def get_connection_string() -> str:
    user = os.environ["POSTGRES_USER"]
    password = os.environ["POSTGRES_PASSWORD"]
    host = os.environ["POSTGRES_HOST"]
    port = os.environ["POSTGRES_PORT"]
    database = os.environ["POSTGRES_DB"]
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

@contextmanager
def get_connection():
    conn = psycopg.connect(get_connection_string())
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == "__main__":
    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT current_database(), current_user, version()")
            print(cursor.fetchone())