# import traceback
def analyze_rates(rates, margin=0.05):
    # traceback.print_stack(limit=5)
    sort_rates = sorted(rates, key=lambda x: float(x["exchange_rate"]), reverse=True)
    best_changer = sort_rates[0]
    best_rate = best_changer["rate"]
    min_rate = float(best_changer.get('rate')) * (1-margin)
    result = []
    for r in sort_rates:
        rate = float(r["rate"])
        if r["rate"] == best_rate:
            r["tag"] = "BEST"
        elif rate > min_rate:
            r["tag"] = "GOOD"
        else:
            r["tag"] = "" 
        result.append(r)
    return result

def calculate_reverse_spread(direct_rates, reverse_rates):
    if not direct_rates or not reverse_rates:
        return None
    spreads = []
    for direct, reverse in zip(direct_rates, reverse_rates):
        direct_rate = float(direct["rate"])
        reverse_rate = float(reverse["rate"])
        if reverse_rate == 0:
            spread = None
            continue
        spread = (1 - (direct_rate / reverse_rate)) * 100
        spreads.append(spread)
    return spreads