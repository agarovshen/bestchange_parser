def calculate_spreads(direct_values, reverse_values):
    if not direct_values or not reverse_values:
        return []
    spreads = []
    if len(direct_values) != len(reverse_values):
        raise ValueError("Direct and reverse length must be equal")
    for direct_value, reverse_value in zip(direct_values, reverse_values):
        if reverse_value == 0:
            continue
        spread = round((1 - direct_value * reverse_value) * 100, 2)
        spreads.append(spread)
    return spreads
#########################################################################
def generate_pairs_list(currency_ids):
    pairs_list = []
    for i, from_id in enumerate(currency_ids):
        for to_id in currency_ids[i+1:]:
            pairs_list.append(f"{from_id}-{to_id}")
            pairs_list.append(f"{to_id}-{from_id}")
    return pairs_list