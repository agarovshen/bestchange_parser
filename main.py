from api import get_rates_by_name
# from formatter import format_changer
from logic import analyze_rates
from gui import get_currency_codes, show_rates
def main():
    from_code, to_code = get_currency_codes()
    rates = get_rates_by_name(from_code,to_code)
    result = analyze_rates(rates)
    result = result[:7]
    show_rates(result)
    # 
    # for r in result:
    #     print_changer(r)
main()