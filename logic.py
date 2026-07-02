def sort_rates(rates):
    sorted_rates = sorted(rates, key=lambda x: float(x["rate"]), reverse=True)
    return sorted_rates

def filter_rates(rates, margin=0.02):
    best_changer = rates[0]
    min_rate = float(best_changer.get('rate')) * (1-margin)
    return best_changer, min_rate