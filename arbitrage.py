from models import Rates, ExchangeDirection, ExchangeCycle
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
    def prepare_exchange_data(self):
        pairs = generate_pairs_list(self.currency_ids)
        print("arbitrage.py len of pairs before", len(pairs))
        directions_data = self.repository.get_directions(pairs)
        rates_data = self.repository.get_rates(pairs, directions_data)
        print("arbitrage.py len of rates_data", len(rates_data))
        rates_by_direction = {}
        for rate in rates_data:
            rates_by_direction.setdefault(rate["direction_id"], []).append(rate)
        pairs = {
            (d["from_currency_id"], d["to_currency_id"])
            for d in rates_data
        }
        print("arbitrage.py after pairs len", len(pairs))       
        return pairs, directions_data, rates_by_direction
    ###################################################################
    def create_direction(self, pair, rates_by_direction, directions_by_pair):
        direction = directions_by_pair[pair]
        direction_id = direction["direction_id"]
        return ExchangeDirection(rates_by_direction[direction_id], direction)
    def create_directions(self, pairs, directions_data, rates_by_direction):

        valid_two_directions = [
            d for d in directions_data
            if (d["from_currency_id"], d["to_currency_id"]) in pairs
            and (d["to_currency_id"], d["from_currency_id"]) in pairs
        ]
        return [
            ExchangeDirection(Rates(rates_by_direction[valid_direction["direction_id"]]), valid_direction)
            for valid_direction in valid_two_directions
        ]
    ###################################################################
    def create_cycles(self, pairs, directions_data, rates_by_direction):
        directions_by_pair = {
            (d["from_currency_id"], d["to_currency_id"]):d
            for d in directions_data
        }
        print("arbtirage.py len of directions by pair", len(directions_by_pair))
        valid_three_pairs = [
            (a,b,c)
            for a,b in pairs
            for x,c in pairs
            if x==b and (c,a) in pairs
        ]
        print("arbitrage.py valid three pairs list of pairs", len(valid_three_pairs))
        return [
            ExchangeCycle(
                (self.create_direction((a,b), rates_by_direction, directions_by_pair)),
                (self.create_direction((b,c), rates_by_direction, directions_by_pair)),
                (self.create_direction((c,a), rates_by_direction, directions_by_pair))
            )
            for a,b,c in valid_three_pairs
        ]
    ######################################################################
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
    def scan_for_two_directions(self, directions):
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
        return sorted(result, key=lambda x: x["spread"][0], reverse=True)
    ######################################################################
    def scan_for_cycles(self, cycles):
        pass
    ######################################################################
    def search(self,directions_var = 2):
        pairs, directions_data, rates_by_direction = self.prepare_exchange_data()        
        if directions_var == 2:
            result = []
            directions = self.create_directions(pairs,directions_data,rates_by_direction)       
            return self.scan_for_two_directions(directions)
        elif directions_var == 3:
            result = []
            cycles = self.create_cycles(pairs, directions_data, rates_by_direction)
            return result