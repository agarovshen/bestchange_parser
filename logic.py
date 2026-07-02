def analyze_rates(rates, margin=0.05):
    sort_rates = sorted(rates, key=lambda x: float(x["rate"]), reverse=True)
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