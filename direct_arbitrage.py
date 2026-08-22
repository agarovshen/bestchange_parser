from models import ExchangeDirection
from logic import calculate_spreads


def create_directions(pairs, directions_data, rates_objects_by_direction):

    valid_two_directions = [
        d for d in directions_data
        if (d["from_currency_id"], d["to_currency_id"]) in pairs
        and (d["to_currency_id"], d["from_currency_id"]) in pairs
    ]
    return [
        ExchangeDirection(rates_objects_by_direction[valid_direction["direction_id"]], valid_direction)
        for valid_direction in valid_two_directions
    ]
##################################################################################

def find_spreads(direct, reverse):
    # Prepare rates and calculate spread between two directions.
    direct_rates = [
        rate.rate
        for rate in direct
    ]
    reverse_rates = [
        rate.rate
        for rate in reverse
    ]
    spreads = calculate_spreads(direct_rates,reverse_rates)
    return spreads
######################################################################
def scan_for_two_directions(directions):
    result = []
    for i in range(0, len(directions), 2):
        direct_rates = directions[i].rates.select_cheapest(top=1)
        reverse_rates = directions[i+1].rates.select_cheapest(top=1)
        direction = {
                "direct": directions[i],
                "reverse": directions[i+1],
                "direct_rates": direct_rates,
                "reverse_rates": reverse_rates,
                "spread": find_spreads(direct_rates, reverse_rates),
                "profit": "future soon"
            }
        result.append(direction)
    return sorted(result, key=lambda x: x["spread"][0], reverse=True)
