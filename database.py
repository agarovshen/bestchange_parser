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
        self.create_currencies_table(cursor)
        self.create_directions_table(cursor)
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
                direction_id INTEGER,
                changer_id INTEGER,
                rate REAL,
                inmin REAL,
                inmax REAL,
                UNIQUE(direction_id, changer_id),
                FOREIGN KEY(direction_id)
                    REFERENCES directions(id),
                FOREIGN KEY(changer_id)
                    REFERENCES changers(id)
            )""")
    ###################################################
    def load_rates(self, directions):
        conn = self.connect()
        cursor = conn.cursor()
        rates = []
        for direction in directions:
            direction_id = direction["direction_id"]
            cursor.execute("""
                SELECT 
                    rates.direction_id, 
                    changers.name, 
                    from_currency.currency_id, 
                    to_currency.currency_id, 
                    rates.rate, 
                    rates.inmin, 
                    rates.inmax
                FROM rates
                JOIN changers
                    ON rates.changer_id = changers.changer_id
                JOIN directions
                    ON rates.direction_id = directions.id
                JOIN currencies AS from_currency
                    ON directions.from_currency_id = from_currency.currency_id
                JOIN currencies as to_currency
                    ON directions.to_currency_id = to_currency.currency_id
                WHERE direction_id = ? """,
                (direction_id,))
            rows = cursor.fetchall()
            rates.extend(rows)
        conn.close()
        return rates
    ###################################################
    def save_rates(self, rates_data):
        conn = self.connect()
        cursor = conn.cursor()
        for direction, rates in rates_data.items():
            from_currency_id, to_currency_id = direction.split("-")
            cursor.execute("""
                SELECT id 
                FROM directions
                WHERE from_currency_id = ? 
                AND to_currency_id = ? """,
                (from_currency_id, to_currency_id))
            row = cursor.fetchone()
            if row is None:
                continue
            direction_id = row[0]

            cursor.execute("""
                DELETE FROM rates
                WHERE direction_id = ? """, 
                (direction_id,))
            for rate in rates:
                cursor.execute("""
                    INSERT INTO rates(
                        direction_id,
                        changer_id,
                        rate,
                        inmin,
                        inmax)
                        VALUES(?,?,?,?,?)""",
                        (
                            direction_id,
                            rate["changer"],
                            rate["rate"],
                            rate["inmin"],
                            rate["inmax"]
                        ))
        conn.commit()
        conn.close()
    ###################################################
    def create_directions_table(self, cursor):
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS directions(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_currency_id INTEGER,
                to_currency_id INTEGER,
                UNIQUE(from_currency_id, to_currency_id),
                FOREIGN KEY(from_currency_id)
                    REFERENCES curencies(id),
                FOREIGN KEY(to_currency_id)
                    REFERENCES currencies(id)
                )
                """)
    ###################################################
    def save_directions(self,pairs):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.executemany("""
        INSERT OR IGNORE INTO directions(
            from_currency_id,
            to_currency_id)
            VALUES(?,?) """,
            [pair.split("-") for pair in pairs])
        conn.commit()
        conn.close()
    ###################################################
    def load_directions(self, pairs):
        conn = self.connect()
        cursor = conn.cursor()
        conditions = " OR ".join(
            "(from_currency_id = ? AND to_currency_id = ?)"
            for _ in pairs
        )
        values = [value for pair in pairs for value in pair.split("-")]
        cursor.execute(f"""
            SELECT 
                directions.id, 
                directions.from_currency_id, 
                directions.to_currency_id, 
                from_currency.code, 
                to_currency.code
            FROM directions 
            JOIN currencies as from_currency
                ON directions.from_currency_id = from_currency.currency_id
            JOIN currencies as to_currency
                ON directions.to_currency_id = to_currency.currency_id
            WHERE {conditions} """,
            values)
        rows = cursor.fetchall()
        conn.close()
        return rows
        # When loading rates:
# SELECT
#     rates.*,
#     changers.name
# FROM rates
# JOIN changers
# ON rates.changer_id = changers.changer_id;