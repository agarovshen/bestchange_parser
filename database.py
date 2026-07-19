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
                   changer_name TEXT,
                   rate REAL,
                   exchange_rate REAL,
                   inmin REAL,
                   reserve REAL)
                   """)
    conn.commit()
    conn.close()

def check_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(rates)")

    for column in cursor.fetchall():
        print(column)
    
    conn.commit()
    conn.close()
def save_direction(direction):
    conn = get_connection()
    cursor = conn.cursor()

    for rate in direction.rates:
        cursor.execute("""
            INSERT INTO rates(
                       from_code,
                       to_code,
                       changer_name,
                       rate,
                       exchange_rate,
                       inmin,
                       reserve
                       )
                       VALUES(?,?,?,?,?,?,?)
                       """,
                       (
                           direction.from_code,
                           direction.to_code,
                           rate["changer_name"],
                           rate["rate"],
                           rate["exchange_rate"],
                           rate["inmin"],
                           rate["reserve"]
                       ))
    conn.commit()
    conn.close()