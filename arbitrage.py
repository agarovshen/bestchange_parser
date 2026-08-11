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
    def create_directions(self, from_code, to_code):
        # Create one exchange direction (A -> B) with loaded rates.
        # Used for direct, reverse and future route calculations.
        from_currency = self.currencies.id_by_code[from_code]
        to_currency = self.currencies.id_by_code[to_code]
        pair = from_currency.currency_id, to_currency.currency_id
        pairs = generate_pairs_list(pair)
        directions_data = self.repository.get_directions(pairs)
        rates_data = self.repository.get_rates(pairs, directions_data)
        rates_by_direction = {}
        for rate in rates_data:
            direction_id = rate["direction_id"]
            rates_by_direction.setdefault(direction_id, []).append(rate)
        return[
            ExchangeDirection(Rates(rates_by_direction[direction_data["direction_id"]]), direction_data)
            for direction_data in directions_data
        ]
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
        directions = self.create_directions(from_code, to_code)
        print("directions from arbitrage.py", directions)
        # directions = [
        #     direction.rates.select_cheapest(top=3)
        #     for direction in directions
        # ]
        # direction = direction.with_rates(direction.rates.select_cheapest(top=3))  
        return directions