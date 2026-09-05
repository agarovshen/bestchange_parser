from models import ArbitrageCycle, ExchangeCycle
from logic import calculate_cycle_spreads

import time

def create_cycles(valid_rates):

    valid_three_pairs = [
        (a,b,c)
        for a,b in valid_rates.keys()
        for x,c in valid_rates.keys()
        if x == b and (c,a) in valid_rates.keys() and a < b and a < c
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
    start_time = time.perf_counter()

    for cycle in cycles:
        rate_ab = cycle.direction_ab.best_rate
        rate_bc = cycle.direction_bc.best_rate
        rate_ca = cycle.direction_ca.best_rate
        spread = calculate_cycle_spreads(rate_ab.rate, rate_bc.rate, rate_ca.rate)
        if spread <= 1:
            continue
        result_cycle = ArbitrageCycle(
            direction_ab_name= rate_ab.direction,
            direction_bc_name= rate_bc.direction,
            direction_ca_name= rate_ca.direction,
            direction_ab_changer=rate_ab.changer.name,
            direction_bc_changer=rate_bc.changer.name,
            direction_ca_changer=rate_ca.changer.name,
            direction_ab_rate=rate_ab.rate,
            direction_bc_rate=rate_bc.rate,
            direction_ca_rate=rate_ca.rate,
            spread=spread,
            profit_estimate="future soon"
        )
        result.append(result_cycle)

    result.sort(key=lambda x: x.spread, reverse=True)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    print(f"Сканирование циклов завершено за {execution_time:.3f} секунд")
    return result