import sqlite3
DB_NAME = "rates.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS rates (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   from_code TEXT,
                   to_code TEXT,
                   changer_name TEXT
                   rate REAL,
                   exchange_rate REAL,
                   inmin REAL)
                   """)
    conn.commit()
    conn.close()