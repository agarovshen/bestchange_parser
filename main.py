# from api import get_rates
from logic import calculate_reverse_spreads
from gui import run_app
from database import Database

def main():
    db = Database()
    db.create_tables()
    db.check_table()
    def handle_search(from_code, 
                      to_code, 
                      show_reverse_rates_enabled=False, 
                      calculate_spreads_enabled=False):
        
        direct_direction = db.load_direction(from_code, to_code)
        reverse_direction = db.load_direction(to_code, from_code)
        # direct_direction, reverse_direction = get_rates(from_code, to_code)
        # print(f"main.py direct direction -> {direct_direction.rates} \n"
        #       f"reverse direction --> {reverse_direction.rates}")
        # save_direction(direct_direction)
        # save_direction(reverse_direction)
        # test = load_direction(from_code, to_code)
        # print("test rezult", test)
        # print("test rates rezult", test.rates[:2])
        direct_direction.select_best(top=3)
        if show_reverse_rates_enabled or calculate_spreads_enabled:
            reverse_direction.select_cheapest(top=3)
        spreads = calculate_reverse_spreads(direct_direction.selected_rates, reverse_direction.selected_rates)
        return direct_direction, reverse_direction, spreads
    run_app(handle_search)
main()