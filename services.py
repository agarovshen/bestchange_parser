from api import load_rates
from models import ExchangeDirection, Rates
from logic import calculate_spreads

class ExchangeServices:
    def __init__(self, changers, currencies):
        # Store shared exchange data used to build directions.
        self.changers = changers
        self.currencies = currencies
    ##########################################################################
    def create_direction(self, from_code, to_code):
        # Create one exchange direction (A -> B) with loaded rates.
        # Used for direct, reverse and future route calculations.
        from_currency = self.currencies.get_by_code(from_code)
        to_currency = self.currencies.get_by_code(to_code)
        rates_data = load_rates(from_currency.currency_id, to_currency.currency_id)        
        for rate in rates_data:
            rate["changer_name"] = self.changers.changers_map[rate["changer"]]
        rates = Rates(rates_data)

        direction = ExchangeDirection(from_currency, to_currency, rates)
        return direction
    ##########################################################################
    def find_spreads(self, direct, reverse):
        # Prepare rates and calculate spread between two directions.
        direct_rates = [
            rate.rate
            for rate in direct.rates
        ]
        reverse_rates = [
            rate.rate
            for rate in reverse.rates
        ]
        spreads = calculate_spreads(direct_rates,reverse_rates)
        return spreads
    ###########################################################################
    def search(self, from_code, to_code, show_reverse_rates_enabled=False, calculate_spreads_enabled=False):
        # Main service method used by GUI.
        # Creates required directions and optional spread calculation.
        direct = self.create_direction(from_code, to_code)
        direct = direct.with_rates(direct.rates.select_cheapest(top=3))
        reverse = None
        spreads = []
        if show_reverse_rates_enabled or calculate_spreads_enabled:
            reverse = self.create_direction(to_code, from_code)
            reverse = reverse.with_rates(reverse.rates.select_cheapest(top=3))
        if calculate_spreads_enabled:
            spreads = self.find_spreads(direct, reverse)
        return direct, reverse, spreads