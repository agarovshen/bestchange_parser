from api import get_data, load_rates
from database import Database

class ExchangeRepository():
    def __init__(self):
        self.db = Database()
        self.db.create_tables()
    ##################################################
    def get_changers(self):
        changers_data = self.db.load_changers()
        if not changers_data:
            print("changers loading from api: repository.py")
            changers_data = get_data("changers")
            self.db.save_changers(changers_data)
            changers_data = self.db.load_changers()
        return [
            {
                "id": changer_id,
                "name": name
            }
            for changer_id, name in changers_data
        ]
    ##################################################
    def get_currencies(self):
        currencies_data = self.db.load_currencies()
        if not currencies_data:
            currencies_data = get_data("currencies")
            self.db.save_currencies(currencies_data)
            currencies_data = self.db.load_currencies()
        return [
            {
                "id": currency_id,
                "name": name,
                "viewname": viewname,
                "code": code
            }
            for currency_id, name, viewname, code in currencies_data
        ]
    ######################################################
    def get_rates(self, pairs, directions):
        rates_data = self.db.load_rates(directions)
        if not rates_data:
            print("Loading from api: repository.py not rates in db")
            rates_data = {}
            for i in range(0, len(pairs), 500):
                batch = pairs[i:i + 500]
                batch = "+".join(batch)
                batches_data = load_rates(batch)
                rates_data.update(batches_data)
            self.db.save_rates(rates_data)
            rates_data = self.db.load_rates(directions)
        return [
            {
                "direction_id": direction_id,
                "changer": changer_name,
                "from_currency_id": from_currency_id,
                "to_currency_id": to_currency_id,
                "rate": rate,
                "inmin": inmin,
                "inmax": inmax
            }
            for direction_id, changer_name, from_currency_id, to_currency_id, rate, inmin, inmax in rates_data  
        ]
    ##############################################################
    def get_directions(self, pairs):
        result = []
        for i in range(0, len(pairs), 500):
            banch = pairs[i:i + 500]
            directions_data = self.db.load_directions(banch)
            if not directions_data:
                self.db.save_directions(banch)
                directions_data = self.db.load_directions(banch)
            result.extend(directions_data)
        return [
            {
                "direction_id": id,
                "from_currency_id": from_currency_id,
                "to_currency_id": to_currency_id,
                "from_currency_code": from_currency_code,
                "to_currency_code": to_currency_code
            }
            for id, from_currency_id, to_currency_id, from_currency_code, to_currency_code in result      
        ]