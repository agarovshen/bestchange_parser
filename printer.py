from logic import filter_rates

def print_changer(r, prefix=""):
    print(
        f"{prefix} Changer: {r.get('changer')}"
        f"|Rate: {r.get('rate')}"
        f"|Inmax: {r.get('inmax')}"
        f"|Inmin: {r.get('inmin')}")
    return

def print_rates(rates, margin=0.02):
    print("=== BESTCHANGE PARSER ===")
    if not rates:
        print("No rates found")
        return
    best_changer, min_rate = filter_rates(rates)
    print_changer(best_changer, "BEST")
    for r in rates[1:]:
        if float(r.get('rate')) > min_rate:
            print_changer(r, "GOOD")
        else: 
            print_changer(r)