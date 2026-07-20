import sqlite3
from models import ExchangeDirection
class Database:
    def __init__(self, db_name="rates.db"):
        self.db_name = db_name
    ##########################################    
    def get_connection(self):
        return sqlite3.connect(self.db_name)
    ##########################################
    def create_tables(self):
        conn = self.get_connection()
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
    ##########################################
    def check_table(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("PRAGMA table_info(rates)")

        for column in cursor.fetchall():
            print(column)
        
        conn.commit()
        conn.close()
    ##########################################
    def save_direction(self, direction):
        conn = self.get_connection()
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
    ##########################################
    def load_direction(self, from_code, to_code):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                    SELECT
                    changer_name,
                    rate,
                    exchange_rate,
                    inmin,
                    reserve
                    FROM rates
                    WHERE from_code = ?
                    AND to_code = ?
                """,
                (
                    from_code,
                    to_code
                ))
        rows = cursor.fetchall()
        conn.close()
        rates = []
        for row in rows:
            rates.append({
                "changer_name": row[0],
                "rate": row[1],
                "exchange_rate": row[2],
                "inmin": row[3],
                "reserve": row[4]
            })
        return ExchangeDirection(
            from_code,
            to_code,
            rates
        )
    ##########################################
    def delete_direction(self, from_code, to_code):
        conn = self.get_connection()
        cursor = conn.cursor()

        cursor.execute("""
                        DELETE FROM rates
                        WHERE from_code = ?
                        AND to_code = ?    
                    """,
                    (
                        from_code,
                        to_code
                    ))
        conn.commit()
        conn.close()