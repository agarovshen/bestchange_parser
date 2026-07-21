from api import get_data, load_rates
from logic import calculate_reverse_spreads
from gui import run_app
from models import Currencies, ExchangeDirection, Changers
from database import Database

def main():
    db = Database()
    db.create_tables()
    db.check_table()        
    currencies_data = get_data("currencies")
    changers_data = get_data("changers")
    changers = Changers(changers_data)
    currencies = Currencies(currencies_data)
    def create_direction(from_currency, to_currency):
        rates = load_rates(from_currency.currency_id, 
                           to_currency.currency_id)
        return ExchangeDirection(from_currency, 
                                 to_currency, 
                                 rates)
    def handle_search(from_code, 
                      to_code, 
                      show_reverse_rates_enabled=False, 
                      calculate_spreads_enabled=False):
        
        # direct_direction = db.load_direction(from_code, to_code)
        # reverse_direction = db.load_direction(to_code, from_code)

        from_currency = currencies.get_by_code(from_code)
        to_currency = currencies.get_by_code(to_code)
        direct_direction = create_direction(from_currency,to_currency)
        reverse_direction = create_direction(to_currency, from_currency)
        # direct_direction, reverse_direction = get_ rates(from_code, to_code)
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