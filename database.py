import sqlite3
class Database:
    def __init__(self, name="bestchange.db"):
        self.name = name
    def connect(self):
        return sqlite3.connect(self.name)
    ###################################################
    def create_tables(self):
        conn = self.connect()
        cursor = conn.cursor()
        self.create_changers_table(cursor)
        print("end creating changers table")
        self.create_currencies_table(cursor)
        self.create_rates_table(cursor)
        conn.commit()
        conn.close()
    ###################################################
    def create_changers_table(self,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS changers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                changer_id INTEGER UNIQUE,
                name TEXT
            )""")
    ###################################################
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
    ###################################################
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
    ###################################################
    def create_currencies_table(self,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS currencies(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                currency_id INTEGER UNIQUE,
                name TEXT,
                viewname TEXT,
                code TEXT
            )""")
    ###################################################
    def load_currencies(self):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT currency_id, name, viewname, code
            FROM currencies """)
        rows = cursor.fetchall()
        conn.close()
        return rows
    ###################################################
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
    ###################################################
    def create_rates_table(self,cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS rates(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_currency_id INTEGER NOT NULL,
                to_currency_id INTEGER NOT NULL,
                changer_id INTEGER NOT NULL,
                rate REAL,
                inmin REAL,
                inmax REAL,
                UNIQUE(
                    from_currency_id,
                    to_currency_id, 
                    changer_id
                ),
                FOREIGN KEY(from_currency_id)
                    REFERENCES currencies(currency_id),
                FOREIGN KEY(to_currency_id)
                    REFERENCES currencies(currency_id),
                FOREIGN KEY(changer_id)
                    REFERENCES changers(id)
            )""")
    ###################################################
    def load_rates(self, pairs):
        if not pairs:
            return []
        rates = []
        conn = self.connect()
        cursor = conn.cursor()
        for i in range(0, len(pairs), 500):
            batch = pairs[i:i + 500]
            conditons = " OR ".join(
                """
                (
                    from_currency_id = ?
                    AND to_currency_id = ?
                )
                """
                for _ in batch
            )
            values = [value for pair in batch for value in pair.split("-")]
            cursor.execute(f"""
                SELECT 
                    rates.from_currency_id,
                    rates.to_currency_id, 
                    rates.changer_id, 
                    rates.rate, 
                    rates.inmin, 
                    rates.inmax
                FROM rates
                WHERE {conditons}
            """, values)
            rates.extend(cursor.fetchall())
        
        conn.close()
        return rates
    ###################################################
    def save_rates(self, rates_data):
        conn = self.connect()
        cursor = conn.cursor()
        for direction, rates in rates_data.items():
            from_currency_id, to_currency_id = map(int, direction.split("-"))
            cursor.execute("""
                DELETE FROM rates
                WHERE from_currency_id = ? 
                AND to_currency_id = ? 
                """, (
                        from_currency_id, 
                        to_currency_id
                    )
                )
            for rate in rates:
                cursor.execute("""
                    INSERT INTO rates(
                        from_currency_id,
                        to_currency_id,
                        changer_id,
                        rate,
                        inmin,
                        inmax)
                        VALUES(?,?,?,?,?,?)""",
                        (
                            from_currency_id,
                            to_currency_id,
                            rate["changer"],
                            rate["rate"],
                            rate["inmin"],
                            rate["inmax"]
                        ))
        conn.commit()
        conn.close()