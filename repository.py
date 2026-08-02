from api import get_data, load_rates
from database import Database

class ExchangeRepository():
    def __init__(self):
        self.db = Database()
        self.db.create_tables()
    ##################################################
    def get_changers(self):
        changers_data = get_data("changers")
        self.db.save_changers(changers_data)
        return changers_data
    ##################################################
    def get_currencies(self):
        currencies_data = get_data("currencies")
        self.db.save_currencies(currencies_data)
        return currencies_data
    def get_rates(self, from_currency, to_currency):
        rates_data = load_rates(from_currency.currency_id, to_currency.currency_id)
        self.db.save_rates(from_currency.code, to_currency.code, rates_data)
        return rates_data