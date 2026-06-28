from api import get_currencies
from printer import print_currencies
def main():
    currencies = get_currencies()
    print_currencies(currencies)
    print ("\n Goctov \n")
main()