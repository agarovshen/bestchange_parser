from models import Rates, Currencies, Changers
from logic import generate_pairs_list
from triangle_arbitrage import create_cycles, scan_for_cycles
from direct_arbitrage import scan_for_two_directions
class ArbitrageScanner:
    def __init__(self, repository):
        self.repository = repository
        self.currencies = Currencies(repository.currencies)
        self.changers = Changers(repository.changers)
        self.currency_ids = [
            93,43,73,172,139,212,106,126,160,99,161,149,115,138,140,36,10,208,180,268,313,314,
            315,169,163,256,306,23,110,235,228,269,47,257,214,24,267,189,203,206,143,87,173,162,
            177,178,179,181,182,185,133,48,124,168,16,19,104,134,27,61,135,26,197,198,175,201,
            202,205,82,209,316,286,130,129,186,295,282,323,184,325,310
        ]#1
        self.pairs = generate_pairs_list(self.currency_ids)
    ##################################################################
    def prepare_exchange_data(self):
        rates_data = self.repository.get_rates(self.pairs)

        rates_by_direction = {}

        for rate in rates_data:
            from_id = rate["from_currency_id"]
            to_id = rate["to_currency_id"]
            rate["changer"] = self.changers.changers_map[rate["changer_id"]]
            rate["from_currency"] = self.currencies.currencies_map[rate["from_currency_id"]]
            rate["to_currency"] = self.currencies.currencies_map[rate["to_currency_id"]]
            del rate["changer_id"]
            del rate["from_currency_id"]
            del rate["to_currency_id"]
            rates_by_direction.setdefault((from_id, to_id), []).append(rate)

        valid_rates = {
            pair: Rates(rates) 
            for pair, rates in rates_by_direction.items() 
            if (pair[1], pair[0]) in rates_by_direction 
        }
        return valid_rates
 
    ######################################################################
    def search(self, settings, directions_var = 2):
        valid_rates = self.prepare_exchange_data() 

        if directions_var == 2:
            return scan_for_two_directions(valid_rates)
        
        elif directions_var == 3:
            cycles = create_cycles(pairs, directions_data, rates_objects_by_direction)
            return scan_for_cycles(cycles)