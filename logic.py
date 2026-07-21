def calculate_spreads(direct_values, reverse_values):
    if not direct_values or not reverse_values:
        return []
    spreads = []
    if len(direct_values) != len(reverse_values):
        raise ValueError("Direct and reverse length must be equal")
    for direct_value, reverse_value in zip(direct_values, reverse_values):
        if reverse_value == 0:
            continue
        spread = ((direct_value / reverse_value) - 1 ) * 100
        spreads.append(spread)
    return spreads