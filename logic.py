def calculate_spreads(direct_values, reverse_values):
    if not direct_values or not reverse_values:
        return []
    spreads = []
    if len(direct_values) != len(reverse_values):
        raise ValueError("Direct and reverse length must be equal")
    for direct_value, reverse_value in zip(direct_values, reverse_values):
        if reverse_value == 0:
            continue
        spread = (1 - direct_value * reverse_value) * 100
        spreads.append(spread)
    return spreads
#########################################################################
def generate_pairs_list(currency_ids):
    pairs_list = []
    for from_id in currency_ids:
        for to_id in currency_ids:
            if from_id != to_id:
                pairs_list.append(f"{from_id}-{to_id}")
    return "+".join(pairs_list)
   