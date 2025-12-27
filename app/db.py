import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "localhost"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "stock_db"),
    "user": os.getenv("DB_USER", "stock_user"),
    "password": os.getenv("DB_PASSWORD", "stock_pass"),
}


def get_connection():
    return psycopg2.connect(cursor_factory=RealDictCursor, **DB_CONFIG)

