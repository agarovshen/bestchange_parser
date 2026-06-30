from api import get_rates_by_name
from printer import print_rates
def main():
    print("=== BESTCHANGE PARSER ===")
    from_code = input("From currency: ")
    to_code = input("To currency: ")
    rates = get_rates_by_name(from_code,to_code)
    print_rates(rates)
    print ("\n Ready \n")
main()