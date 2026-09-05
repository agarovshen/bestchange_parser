from bestchange_api import fetch_data, fetch_rates
from database import Database

class ExchangeRepository():
    def __init__(self):
        self.db = Database()
        self.db.create_tables()
        self.currencies = self.get_currencies()
        self.changers = self.get_changers()
    ##################################################
    def get_changers(self):
        changers_data = self.db.load_changers()
        if not changers_data:
            changers_data = fetch_data("changers")
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
            currencies_data = fetch_data("currencies")
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
    def get_rates(self, pairs):
        rates_data = self.db.load_rates(pairs)
        if not rates_data:
            rates_data = {}
            for i in range(0, len(pairs), 500):
                batch = pairs[i:i + 500]
                batch = "+".join(batch)
                batches_data = fetch_rates(batch)
                rates_data.update(batches_data)
            self.db.save_rates(rates_data)
            rates_data = self.db.load_rates(pairs)
        return [
            {
                "from_currency_id": from_currency_id,
                "to_currency_id": to_currency_id,
                "changer_id": changer_id,
                "rate": rate,
                "inmin": inmin,
                "inmax": inmax
            }
            for from_currency_id, to_currency_id, changer_id, rate, inmin, inmax in rates_data  
        ]