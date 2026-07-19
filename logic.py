def calculate_reverse_spreads(direct_rates, reverse_rates):
    if not direct_rates or not reverse_rates:
        return None
    spreads = []
    for direct, reverse in zip(direct_rates, reverse_rates):
        direct_rate = float(direct["exchange_rate"])
        reverse_rate = float(reverse["exchange_rate"])
        if reverse_rate == 0:
            spread = None
            continue
        spread = ((direct_rate / reverse_rate) - 1 ) * 100
        spreads.append(spread)
    return spreads