from models import ExchangeCycle
from logic import calculate_cycle_spreads
def create_direction(pair, rates_objects_by_direction, directions_by_pair):
    direction = directions_by_pair[pair]
    direction_id = direction["direction_id"]
    return ExchangeDirection(rates_objects_by_direction[direction_id], direction)
#################################################################################
def create_cycles(valid_pairs, directions_data, rates_objects_by_direction):
    print("2 arbitrage direction by pair")
    directions_by_pair = {
        (d["from_currency_id"], d["to_currency_id"]):d
        for d in directions_data
    }
    valid_three_pairs = [
        (a,b,c)
        for a,b in valid_pairs
        for x,c in valid_pairs
        if x == b and (c,a) in valid_pairs
    ]
    print("3 before return create cycles arbitrage")
    return [
        ExchangeCycle(
            (create_direction((a,b), rates_objects_by_direction, directions_by_pair)),
            (create_direction((b,c), rates_objects_by_direction, directions_by_pair)),
            (create_direction((c,a), rates_objects_by_direction, directions_by_pair))
        )
        for a,b,c in valid_three_pairs
    ]
####################################################################################
def scan_for_cycles(cycles):
    result = []
    for cycle in cycles:
        direction_ab_rates = cycle.direction_ab.rates.select_cheapest(top=1)[0]
        direction_bc_rates = cycle.direction_bc.rates.select_cheapest(top=1)[0]
        direction_ca_rates = cycle.direction_ca.rates.select_cheapest(top=1)[0]
        result_cycle = {
            "direction_ab": cycle.direction_ab,
            "direction_bc": cycle.direction_bc,
            "direction_ca": cycle.direction_ca,
            "direction_ab_rates": direction_ab_rates,
            "direction_bc_rates": direction_bc_rates,
            "direction_ca_rates": direction_ca_rates,
            "spread": calculate_cycle_spreads(direction_ab_rates.rate, direction_bc_rates.rate, direction_ca_rates.rate)
        }
        result.append(result_cycle)
    return sorted(result, key=lambda x: x["spread"], reverse=True)