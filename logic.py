def sort_rates(rates):
    sorted_rates = sorted(rates, key=lambda x: float(x["rate"]), reverse=True)
    return sorted_rates

def filter_rates(rates, margin=0.02):
    best_changer = rates[0]
    min_rate = float(best_changer.get('rate')) * (1-margin)
    for r in rates:
        if r == best_changer:
            r["tag"] = "BEST"
        elif r > min_rate:
            r["tag"] = "GOOD"
        else:
            r["tag"] = "" 
        result.append(r)
    return result

result = []