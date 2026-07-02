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
    print_changer(best_changer, "BEST")