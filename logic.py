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