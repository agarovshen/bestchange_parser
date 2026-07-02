from api import get_rates_by_name
from printer import print_rates
from logic import sort_rates
def main():
    from_code = input("From currency: ").upper()
    to_code = input("To currency: ").upper()
    rates = get_rates_by_name(from_code,to_code)
    sorted_rates = sort_rates(rates)
    print_rates(sorted_rates)
main()