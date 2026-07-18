from api import get_rates
from logic import calculate_reverse_spread
from gui import run_app

def main():
    def handle_search(from_code, to_code, show_reverse_rates_enabled=False):
        direct_direction, reverse_direction = get_rates(
            from_code, 
            to_code, 
            show_reverse_rates_enabled=show_reverse_rates_enabled)
        direct_direction.select_best(top=3)
        if show_reverse_rates_enabled:
            reverse_direction.select_cheapest(top=3)
        return direct_direction, reverse_direction
    run_app(handle_search)
main()