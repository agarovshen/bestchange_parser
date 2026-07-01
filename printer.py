def print_changer(r, prefix=""):
    print(
        f"{prefix} Changer: {r.get('changer')}"
        f"|Rate: {r.get('rate')}"
        f"|Inmax: {r.get('inmax')}"
        f"|Inmin: {r.get('inmin')}")
def print_rates(rates):
    if not rates:
        print("No rates found")
        return
    best_changer = rates[0]
    min_rate = float(best_changer['rate']) - float(best_changer['rate']) * 0.02
    print_changer(best_changer, "BEST")
    for r in rates[1:]:
        if float(r.get('rate')) > min_rate:
            print_changer(r, "GOOD")
        else: 
            print_changer(r)