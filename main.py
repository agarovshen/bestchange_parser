from api import get_rates
from logic import analyze_rates
from gui import run_app

def main():
    def handle_search(from_code, to_code, use_reverse_spread=False):
        direct_rates, reverse_rates = get_rates(
            from_code, 
            to_code, 
            use_reverse_spread=use_reverse_spread)
        direct_rates_result = analyze_rates(direct_rates)[:7]
        # print(f"Direct rates: {direct_rates_result} Type: {type(direct_rates_result)}")
        reverse_rates_result = []
        spreads = []
        if use_reverse_spread:
            reverse_rates_result = analyze_rates(reverse_rates)[:7]
        return direct_rates_result, reverse_rates_result
    run_app(handle_search)
main()