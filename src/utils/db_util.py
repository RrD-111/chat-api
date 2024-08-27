import os
from dotenv import load_dotenv
import psycopg2

load_dotenv()

def get_db_connection():
     """
    Create and return a connection to the database.

    Returns:
        psycopg2.extensions.connection: A connection to the PostgreSQL database.
    """
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    return conn
