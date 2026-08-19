from models import Rates, ExchangeDirection
from logic import calculate_spreads, generate_pairs_list
class ArbitrageScanner:
    def __init__(self, changers, currencies, repository):
        self.changers = changers
        self.currencies = currencies
        self.repository = repository
        self.currency_ids_part1 = [93,43,73,172,139,212,106,126,160,99,161,149,115,138,140,36,10,208,180,268,313,314]
        self.currency_ids_part2 = [315,169,163,256,306,23,110,235,228,269,47,257,214,24,267,189,203,206,143,87,173,162]
        self.currency_ids_part3 = [177,178,179,181,182,185,133,48,124,168,16,19,104,134,27,61,135,26,197,198,175,201]
        self.currency_ids_part4 = [202,205,82,209,316,286,130,129,186,295,282,323,184,325,310,1]
        self.currency_ids = [
            93,43,73,172,139,212,106,126,160,99,161,149,115,138,140,36,10,208,180,268,313,314,
            315,169,163,256,306,23,110,235,228,269,47,257,214,24,267,189,203,206,143,87,173,162,
            177,178,179,181,182,185,133,48,124,168,16,19,104,134,27,61,135,26,197,198,175,201,
            202,205,82,209,316,286,130,129,186,295,282,323,184,325,310,1
        ]
    ##################################################################
    def create_directions(self, currency_ids):
        pairs = generate_pairs_list(currency_ids)
        directions_data = self.repository.get_directions(pairs)
        rates_data = self.repository.get_rates(pairs, directions_data)
        pairs = {
            (d["from_currency_id"], d["to_currency_id"])
            for d in rates_data
        }
        rates_by_direction = {}
        for rate in rates_data:
            rates_by_direction.setdefault(rate["direction_id"], []).append(rate)
        
        valid_directions = [
            d for d in directions_data
            if (d["from_currency_id"], d["to_currency_id"]) in pairs
            and (d["to_currency_id"], d["from_currency_id"]) in pairs
        ]
        
        print("length of directions", len(directions_data))
        print("length of existing rates_by_direction", len(rates_by_direction))
        print("length of valid directions", len(valid_directions))
        return [
            ExchangeDirection(Rates(rates_by_direction[valid_direction["direction_id"]]), valid_direction)
            for valid_direction in valid_directions
        ]
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
            directions = self.create_directions(self.currency_ids)
            print(len(directions))
        # else:
        #     directions = self.create_directions(from_code, to_code)
        result = []       
        for i in range(0, len(directions), 2):
            direct_rates = directions[i].rates.select_cheapest(top=1)
            reverse_rates = directions[i+1].rates.select_cheapest(top=1)
            direction = {
                    "direct": directions[i],
                    "reverse": directions[i+1],
                    "direct_rates": direct_rates,
                    "reverse_rates": reverse_rates,
                    "spread": self.find_spreads(direct_rates, reverse_rates)
                }
            result.append(direction)
            result.sort(key=lambda direction: direction["spread"][0], reverse=True)

        return result