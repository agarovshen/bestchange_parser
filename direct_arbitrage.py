from models import ExchangeDirection, ArbitragePair
from logic import calculate_spread


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

######################################################################
def scan_for_two_directions(directions, settings):
    print("5. Start scan two directions")
    capital_rates_by_currencies = {
        direction.from_currency_id : direction.rates.select_cheapest(top=1)
        for direction in directions
        if direction.to_currency_id == settings.currency
    }
    result = []
    for i in range(0, len(directions), 2):
        if directions[i+1].from_currency_id  == settings.currency or directions[i].from_currency_id == settings.currency:
            continue
        direct_rate = directions[i].rates.select_cheapest(top=1)[0]
        reverse_rate = directions[i+1].rates.select_cheapest(top=1)[0]
        pair = ArbitragePair(
            direct_name=str(directions[i]),
            reverse_name=str(directions[i+1]),
            best_direct_rate=direct_rate,
            best_reverse_rate=reverse_rate,
            spread=calculate_spread(direct_rate.rate, reverse_rate.rate),
            profit_estimate="Future soon"
        )
        result.append(pair)
    
    print("6. ready scan two directions length of result", len(result))
    return sorted(result, key=lambda x: x.spread, reverse=True)
