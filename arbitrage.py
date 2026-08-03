from models import Rates, ExchangeDirection
from logic import calculate_spreads, generate_pairs_list
class ArbitrageScanner:
    def __init__(self, changers, currencies, repository):
        self.changers = changers
        self.currencies = currencies
        self.repository = repository
        self.currency_ids_part1 = [93,43,73,172,139,212,
                                   106,126,160,99,161,149,
                                   115,138,140,36,10,208,
                                   180,268,313,314]
    ##################################################################
    def create_direction(self, from_code, to_code):
        # Create one exchange direction (A -> B) with loaded rates.
        # Used for direct, reverse and future route calculations.
        from_currency = self.currencies.id_by_code[from_code]
        to_currency = self.currencies.id_by_code[to_code]
        pair = from_currency.currency_id, to_currency.currency_id
        pair_list = generate_pairs_list(pair)
        rates_data = self.repository.get_rates(from_code, to_code, pair_list)
        rates = Rates(rates_data)
        direction = ExchangeDirection(from_currency, to_currency, rates)
        return direction
    ###################################################################
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
    ######################################################################
    def search(self, from_code, to_code, calculate_spreads_enabled=False, find_best_spreads_var=False):
        # Main service method used by GUI.
        # Creates required directions and optional spread calculation.
        direct = self.create_direction(from_code, to_code)
        reverse = self.create_direction(to_code, from_code)
        direct = direct.with_rates(direct.rates.select_cheapest(top=3))
        reverse = reverse.with_rates(reverse.rates.select_cheapest(top=3))
        # if find_best_spreads_var:
        #     for from_id in self.currency_ids_part1:
        #         for to_id in self.currency_ids_part1:
                    
        #     direct = self.create_direction()
        spreads = []                       
        if calculate_spreads_enabled:
            spreads = self.find_spreads(direct, reverse)
        return direct, reverse, spreads