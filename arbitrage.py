from models import Rates, ExchangeDirection
from logic import calculate_spreads, generate_pairs_list
class ArbitrageScanner:
    def __init__(self, changers, currencies, repository):
        self.changers = changers
        self.currencies = currencies
        self.repository = repository
        self.currency_ids_part1 = [93,43,73,172,139,212,106,126,160,99,161,149,115,138,140,36,10,208,180,268,313,314]
    ##################################################################
    def create_directions(self, currency_ids):
        # Create one exchange direction (A -> B) with loaded rates.
        # Used for direct, reverse and future route calculations.
        # from_currency = self.currencies.id_by_code[from_code]
        # to_currency = self.currencies.id_by_code[to_code]
        # pair = from_currency.currency_id, to_currency.currency_id
        pairs = generate_pairs_list(currency_ids)
        directions_data = self.repository.get_directions(pairs)
        rates_data = self.repository.get_rates(pairs, directions_data)
        # print("arbitrage.py", rates_data)
        rates_by_direction = {}
        for rate in rates_data:
            rates_by_direction.setdefault(rate["direction_id"], []).append(rate)
        
        directions = [
            ExchangeDirection(Rates(rates_by_direction[direction_data["direction_id"]]), direction_data)
            for direction_data in directions_data
            ]
        # # direct_directions, reverse_directions = directions[::2], directions[1::2]
        # return direct_directions, reverse_directions
        return directions
    ###################################################################
    def find_spreads(self, direct, reverse):
        # Prepare rates and calculate spread between two directions.
        direct_rates = [
            rate.rate
            for rate in direct
        ]
        reverse_rates = [
            rate.rate
            for rate in reverse
        ]
        spreads = calculate_spreads(direct_rates,reverse_rates)
        return spreads
    ######################################################################
    def search(self, from_code, to_code, find_all_spreads=False):
        # Main service method used by GUI.
        # Creates required directions and optional spread calculation.
        if find_all_spreads:
            # direct_directions, reverse_directions = self.create_directions(self.currency_ids_part1)
            directions = self.create_directions(self.currency_ids_part1)
        else:
            directions = self.create_directions(from_code, to_code)
        result = []       
        for i in range(0, len(directions), 2):
            direct_rates = directions[i].rates.select_cheapest(top=3)
            reverse_rates = directions[i+1].rates.select_cheapest(top=3)
            direction = {
                    "direct": directions[i],
                    "reverse": directions[i+1],
                    "direct_rates": direct_rates,
                    "reverse_rates": reverse_rates,
                    "spread": self.find_spreads(direct_rates, reverse_rates)
                }
            result.append(direction)

        return result
        
    