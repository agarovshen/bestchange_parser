from api import get_rates_by_name
from printer import print_rates
def main():
    print("=== BESTCHANGE PARSER ===")
    from_code = input("From currency: ").upper()
    to_code = input("To currency: ").upper()
    rates = get_rates_by_name(from_code,to_code)
    sorted_rates = sorted(rates, key=lambda x: float(x["rate"]), reverse=True)
    print_rates(sorted_rates)
main()