import sqlite3
class Database:
    def __init__(self, name="bestchange.db"):
        self.name = name
    def connect(self):
        return sqlite3.connect(self.name)
    ###########################################
    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()
        self.create_changers_table(cursor)
        self.create_currencies_table(cursor)
        self.create_rates_table(cursor)
        conn.commit()
        conn.close()
    ##########################################
    def load_changers(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT changer_id, name
            FROM changers
            """)
        rows = cursor.fetchall()
        conn.close()
        return rows
    ##################################################
    def create_changers_table(self,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS changers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                changer_id INTEGER UNIQUE,
                name TEXT
            )""")
    #################################################
    def load_currencies(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT currency_id, name, viewname, code
            FROM currencies """)
        rows = cursor.fetchall()
        conn.close()
        return rows
    ################################################
    def create_currencies_table(self,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS currencies(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency_id INTEGER UNIQUE,
                name TEXT,
                viewname TEXT,
                code TEXT
            )""")
    ##############################################
    def save_changers(self, changers_data):
        conn = self.connect()
        cursor = conn.cursor()
        for changer in changers_data:
            cursor.execute("""
                INSERT OR REPLACE INTO changers(
                    changer_id,
                    name)
                    VALUES(?,?)
                    """,
                    (
                        changer["id"],
                        changer["name"]
                    ))
        conn.commit()
        conn.close()
    def save_currencies(self, currencies_data):
        conn = self.connect()
        cursor = conn.cursor()
        for currency in currencies_data:
            cursor.execute("""
                INSERT OR REPLACE INTO currencies(
                    currency_id,
                    name,
                    viewname,
                    code)
                    VALUES(?,?,?,?)
                    """,
                    (
                        currency["id"],
                        currency["name"],
                        currency["viewname"],
                        currency["code"]
                    ))
        conn.commit()
        conn.close()
    def create_rates_table(self,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rates(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_currency TEXT,
                to_currency TEXT,
                changer_id INTEGER UNIQUE,
                rate REAL,
                inmin REAL,
                inmax REAL
            )""")
    def save_rates(self, from_currency, to_currency, rates_data):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            DELETE FROM rates
            WHERE from_currency = ?
            AND to_currency = ? """, 
            (from_currency, to_currency))
        for rate in rates_data:
            cursor.execute("""
                INSERT OR REPLACE INTO rates(
                    from_currency,
                    to_currency,
                    changer_id,
                    rate,
                    inmin,
                    inmax)
                    VALUES(?,?,?,?,?,?)""",
                    (
                        from_currency,
                        to_currency,
                        rate["changer"],
                        rate["rate"],
                        rate["inmin"],
                        rate["inmax"]
                    ))
        conn.commit()
        conn.close()
        # When loading rates:
# SELECT
#     rates.*,
#     changers.name
# FROM rates
# JOIN changers
# ON rates.changer_id = changers.changer_id;