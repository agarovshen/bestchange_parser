from models import Rates, Currencies
from logic import generate_pairs_list
from triangle_arbitrage import create_cycles, scan_for_cycles
from direct_arbitrage import scan_for_two_directions, create_directions
class ArbitrageScanner:
    def __init__(self, repository):
        # self.changers = changers
        # self.currencies = currencies
        self.repository = repository
        self.currency_ids = [
            93,43,73,172,139,212,106,126,160,99,161,149,115,138,140,36,10,208,180,268,313,314,
            315,169,163,256,306,23,110,235,228,269,47,257,214,24,267,189,203,206,143,87,173,162,
            177,178,179,181,182,185,133,48,124,168,16,19,104,134,27,61,135,26,197,198,175,201,
            202,205,82,209,316,286,130,129,186,295,282,323,184,325,310
        ]#1
    ##################################################################
    def prepare_exchange_data(self, settings):
        pairs = generate_pairs_list(self.currency_ids)
        directions_data = self.repository.get_directions(pairs)
        rates_data = self.repository.get_rates(pairs, directions_data)
        # capital_currency_id = Currencies.id_by_code(settings.currency)
        # print(capital_currency_id)
        # capital_rates = []
        # for rate_data in rates_data:

        #     if rate_data["inmin"] < settings.capital:
        #         continue
        #     capital_rates.append(rate_data)
        rates_by_direction = {}
        for rate in rates_data:
            rates_by_direction.setdefault(rate["direction_id"], []).append(rate)
        valid_pairs = {
            (d["from_currency_id"], d["to_currency_id"])
            for d in rates_data
        }
        rates_objects_by_direction = {
            direction_id : Rates(rates)
            for direction_id, rates in rates_by_direction.items()
        } 
        print("0 after create Rates objects")
        return valid_pairs, directions_data, rates_objects_by_direction
 
    ######################################################################
    def search(self, settings, directions_var = 2):
        pairs, directions_data, rates_objects_by_direction = self.prepare_exchange_data(settings)        
        if directions_var == 2:
            directions = create_directions(pairs, directions_data, rates_objects_by_direction)       
            return scan_for_two_directions(directions)
        elif directions_var == 3:
            print("1 create cycles arbitrage.py ")
            cycles = create_cycles(pairs, directions_data, rates_objects_by_direction)
            print("4 after create cycles arbitrage.py")
            return scan_for_cycles(cycles)