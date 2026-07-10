from api import get_rates
from logic import analyze_rates, calculate_reverse_spread
from gui import run_app

def main():
    def handle_search(from_code, to_code, use_reverse_spread=False):
        direct_rates, reverse_rates = get_rates(
            from_code, 
            to_code, 
            use_reverse_spread=use_reverse_spread)
        print(f"Use reverse spread: {use_reverse_spread}")
        direct_rates_result = analyze_rates(direct_rates)[:2]
        print(f"Main.py Direct rates for {from_code} to {to_code}: {direct_rates_result}")
        reverse_rates_result = []
        spreads = []
        if use_reverse_spread:
            reverse_rates_result = analyze_rates(reverse_rates)[:2]
            print(f"Main.py Reverse rates for {to_code} to {from_code}: {reverse_rates_result}")
            spreads = calculate_reverse_spread(direct_rates_result, reverse_rates_result)
        return direct_rates_result, reverse_rates_result
    run_app(handle_search)
main()