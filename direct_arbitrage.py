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
def scan_for_two_directions(directions, settings):
    capital_rates_by_currencies = {
        direction.from_currency_id : direction.rates.select_cheapest(top=1)
        for direction in directions
        if direction.to_currency_id == settings.currency
    }
    result = []
    for i in range(0, len(directions), 2):
        if directions[i+1].from_currency_id  == settings.currency or directions[i].from_currency_id == settings.currency:
            continue
        direct_rates = directions[i].rates.select_cheapest(top=1)
        direct_inmin = (capital_rates_by_currencies[directions[i].from_currency_id][0].rate * direct_rates[0].inmin)
        reverse_rates = directions[i+1].rates.select_cheapest(top=1)
        reverse_inmin = capital_rates_by_currencies[directions[i+1].from_currency_id][0].rate * reverse_rates[0].rate
        print({capital_rates_by_currencies[directions[i].from_currency_id][0].rate},"=>",{directions[i].from_currency_code}, "=>", {directions[i].to_currency_code}, direct_inmin, reverse_inmin)
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
