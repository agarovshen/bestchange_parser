from api import load_rates
from models import ExchangeDirection
from logic import calculate_spreads

class ExchangeServices:
    def __init__(self, changers, currencies):
        self.changers = changers
        self.currencies = currencies
    ##########################################################################
    def create_direction(self, from_code, to_code):
        from_currency = self.currencies.get_by_code(from_code)
        to_currency = self.currencies.get_by_code(to_code)
        rates = load_rates(from_currency.currency_id, to_currency.currency_id)
        direction = ExchangeDirection(from_currency, to_currency, rates)
        return direction
    ##########################################################################
    def find_spreads(self, direct, reverse):
        direct_rates = direct.select_best(top=3)
        reverse_rates = reverse.select_cheapest(top=3)
        spreads = calculate_spreads(direct_rates,reverse_rates)
        return spreads
    ###########################################################################
    def search(self, from_code, to_code, show_reverse_rates_enabled=False, calculate_spreads_enabled=False):
        direct = self.create_direction(from_code, to_code)
        reverse = None
        spreads = []
        if show_reverse_rates_enabled or calculate_spreads_enabled:
            reverse = self.create_direction(to_code, from_code)
        if calculate_spreads_enabled:
            spreads = self.find_spreads(direct, reverse)
        return direct, reverse, spreads