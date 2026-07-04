from api import get_rates_by_name
# from formatter import format_changer
from logic import analyze_rates
from gui import run_app



def main():
    # from_code, to_code = run_app()
    def handle_search(from_code, to_code):
        rates = get_rates_by_name(from_code,to_code)
        result = analyze_rates(rates)
        result = result[:7]
        print("fack you", result)
    run_app(handle_search)
main()