from api import get_rates_by_name
from printer import print_changer
from logic import analyze_rates
from gui import run_app
def main():
    from_code = input("From currency: ").upper()
    to_code = input("To currency: ").upper()
    rates = get_rates_by_name(from_code,to_code)
    result = analyze_rates(rates)
    for r in result:
        print_changer(r)
    run_app()
main()