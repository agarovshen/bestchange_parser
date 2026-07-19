import sqlite3
DB_NAME = "rates.db"

def get_connection():
    return sqlite3.connect(DB_NAME)