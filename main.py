from api import get_rates_by_name
from logic import analyze_rates
from gui import run_app

def main():
    def handle_search(from_code, to_code):
        rates = get_rates_by_name(from_code,to_code)
        result = analyze_rates(rates)
        result = result[:7]
        return result
    run_app(handle_search)
main()