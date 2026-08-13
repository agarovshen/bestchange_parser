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
        pairs = "+".join(pairs)
        # print("repository.py pairs ->", pairs, "\n", "directions ->", directions)
        rates_data = self.db.load_rates(directions)
        if not rates_data:
            rates_data = load_rates(pairs)
            self.db.save_rates(rates_data)
            rates_data = self.db.load_rates(directions)
        return [
            {
                "direction_id": direction_id,
                "changer": changer_name,
                "from_currency_code": from_currency_code,
                "to_currency_code": to_currency_code,
                "rate": rate,
                "inmin": inmin,
                "inmax": inmax
            }
            for direction_id, changer_name, from_currency_code, to_currency_code, rate, inmin, inmax in rates_data  
        ]
    ##############################################################
    def get_directions(self, pairs):
        directions_data = self.db.load_directions(pairs)
        if not directions_data:
            self.db.save_directions(pairs)
            directions_data = self.db.load_directions(pairs)
            
        return [
            {
                "direction_id": id,
                "from_currency_id": from_currency_id,
                "to_currency_id": to_currency_id,
                "from_currency_code": from_currency_code,
                "to_currency_code": to_currency_code
            }
            for id, from_currency_id, to_currency_id, from_currency_code, to_currency_code in directions_data      
        ]