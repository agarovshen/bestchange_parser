from api import get_rates_by_name
from printer import print_rates
def main():
    print("=== BESTCHANGE PARSER ===")
    from_code = input("From currency: ").upper()
    to_code = input("To currency: ").upper()
    rates = get_rates_by_name(from_code,to_code)
    for r in rates:
        changer = r.get('changer')
        rate = r.get('rate')
        inmin = r.get('inmin')
        inmax = r.get('inmax')
        print(f"Changer: {changer} |rate: {rate} |imin: {inmin} |imax: {inmax}")
    print ("\n Ready \n")
main()