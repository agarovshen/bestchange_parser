def print_currencies(currencies):
    print ("\n ==CURRENCIES== \n")
    for c in currencies:
        print(f"{c['id']:5} | {c['code']:10} | {c['name']}")