from models import ArbitrageCycle, ExchangeCycle
from logic import calculate_cycle_spreads


def create_cycles(valid_rates):

    valid_three_pairs = [
        (a,b,c)
        for a,b in valid_rates.keys()
        for x,c in valid_rates.keys()
        if x == b and (c,a) in valid_rates.keys()
    ] 
    return [
        ExchangeCycle(
            valid_rates[(a,b)],
            valid_rates[(b,c)], 
            valid_rates[(c,a)]
        )
        for a,b,c in valid_three_pairs
    ]
####################################################################################
def scan_for_cycles(cycles):
    result = []
    def direction_show(rate):
        return f"{rate.from_currency.code} -> {rate.to_currency.code}"
    for cycle in cycles:
        rates = [
            cycle.direction_ab.select_cheapest(),
            cycle.direction_bc.select_cheapest(),
            cycle.direction_ca.select_cheapest()
        ]
        spread = calculate_cycle_spreads(*(rate.rate for rate in rates))
        if spread <= 0:
            continue
        result_cycle = ArbitrageCycle(
            direction_ab_name=direction_show(rates[0]),
            direction_bc_name=direction_show(rates[1]),
            direction_ca_name=direction_show(rates[2]),
            direction_ab_changer=rates[0].changer.name,
            direction_bc_changer=rates[1].changer.name,
            direction_ca_changer=rates[2].changer.name,
            direction_ab_rate=rates[0].rate,
            direction_bc_rate=rates[1].rate,
            direction_ca_rate=rates[2].rate,
            spread=spread,
            profit_estimate="future soon"
        )
        result.append(result_cycle)
    return sorted(result, key=lambda x: x.spread, reverse=True)