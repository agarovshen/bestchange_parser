from models import ArbitragePair
from logic import calculate_spread


######################################################################
def scan_for_two_directions(valid_rates):
    result = []
    rates = list(valid_rates.values())
    for i in range(0, len(valid_rates), 2):
        direct_rate = rates[i].select_cheapest(top=1)[0]
        reverse_rate = rates[i+1].select_cheapest(top=1)[0]
        from_code = direct_rate.from_currency.code
        to_code = direct_rate.to_currency.code
        spread = calculate_spread(direct_rate.rate, reverse_rate.rate)
        if spread > 0:
            pair = ArbitragePair(
                direct_name=f"{from_code}-{to_code}",
                reverse_name=f"{to_code}-{from_code}",
                changer=direct_rate.changer.name,
                best_direct_rate=direct_rate.rate,
                best_reverse_rate=reverse_rate.rate,
                spread=spread,
                profit_estimate="Future soon"
            )
            result.append(pair)
    return sorted(result, key=lambda x: x.spread, reverse=True)