from api import get_rates_by_name
from printer import print_changer
from logic import filter_rates
def main():
    from_code = input("From currency: ").upper()
    to_code = input("To currency: ").upper()
    rates = get_rates_by_name(from_code,to_code)
    filter_rates(rates)
main()