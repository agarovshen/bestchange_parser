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
    def get_rates(self, from_code, to_code, pairs):
        rates_data = load_rates(pairs)
        self.db.save_rates(from_code, 
                           to_code, 
                           rates_data)
        return rates_data
    ##############################################################

    