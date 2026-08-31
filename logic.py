from math import prod
def calculate_spread(direct_value, reverse_value):
    if not direct_value or not reverse_value:
        return None
    return round((1-direct_value * reverse_value) * 100, 2)
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