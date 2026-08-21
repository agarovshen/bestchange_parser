from math import prod
def calculate_spreads(direct_values, reverse_values):
    if not direct_values or not reverse_values:
        return []
    if len(direct_values) != len(reverse_values):
        raise ValueError("Direct and reverse length must be equal")
    return [
        round((1-direct * reverse) * 100, 2)
        for direct, reverse in zip(direct_values, reverse_values)
        if reverse != 0
    ]
#########################################################################
def calculate_cycle_spreads(*rates):
    cycle_rate = prod(rates)
    return (1 - cycle_rate) * 100
#########################################################################
def generate_pairs_list(currency_ids):
    return [
        pair    
        for i, from_id in enumerate(currency_ids) 
        for to_id in currency_ids[i+1:]
        for pair in (f"{from_id}-{to_id}", f"{to_id}-{from_id}")
    ]