from api import load_rates

class ExchangeServices:
    def __init__(self, changers, currencies):
        self.changers = changers
        self.currencies = currencies
    def create_direction(self, from_code, to_code):
        from_currency = self.currencies.get_by_code(from_code)
        to_currency = self.currencies.get_by_code(to_code)
        rates = load_rates(from_currency.currency_id, to_currency.currency_id)