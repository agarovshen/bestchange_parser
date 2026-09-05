from dataclasses import dataclass
from locale import currency
from typing import Optional
class ExchangeCycle:
    def __init__(self, direction_ab, direction_bc, direction_ca):
        self.direction_ab = direction_ab
        self.direction_bc = direction_bc
        self.direction_ca = direction_ca
class Currency:
    def __init__(self, data):
        self.currency = data
        self.name = data["name"]
        self.code = data["code"]
        self.currency_id = data["id"]
    
class Currencies:
    def __init__(self, data):
        self.currencies = [
            Currency(currency)
            for currency in data
        ]
        self.currency_by_id = {
            currency.currency_id: currency
            for currency in self.currencies
        }
        self.currency_by_code = {
            currency.code: currency
            for currency in self.currencies
        }
class Changer:
    def __init__(self, data):
        self.changer = data
        self.changer_id = data["id"]
        self.name = data["name"]

class Changers:
    def __init__(self, data):
        self.changers = [
            Changer(changer)
            for changer in data
        ]
        self.changers_map = {
            changer.changer_id: changer
            for changer in self.changers
        }

@dataclass(slots=True)    
class Rate:
    rate: float
    from_currency: Currency
    to_currency: Currency
    changer: Changer
    inmin: float
    
    @classmethod
    def from_dict(cls, data: dict) -> "Rate":
        return cls(
            rate = float(data["rate"]),
            from_currency = data["from_currency"],
            to_currency = data["to_currency"],
            changer = data["changer"],
            inmin = float(data["inmin"])
        )

class Rates:
    def __init__(self, rates: list[dict]):
        self.rate_objects = [Rate.from_dict(r) for r in rates]
    ##############################################################
    def select_cheapest(self):      
        return min(self.rate_objects, key=lambda r: r.rate)
    ###############################################################
    def select_best(self):
        return max(self.rate_objects, key=lambda r: r.rate, reverse=True)
    
@dataclass(slots=True)
class ArbitragePair:
    direct_name: str
    reverse_name: str
    direct_changer: str
    reverse_changer: str
    best_direct_rate: float
    best_reverse_rate: float
    spread: float
    profit_estimate: float
@dataclass(slots=True)
class ArbitrageCycle:
    direction_ab_name: str
    direction_bc_name: str
    direction_ca_name: str
    direction_ab_changer: str
    direction_bc_changer: str
    direction_ca_changer: str
    direction_ab_rate: float
    direction_bc_rate: float
    direction_ca_rate: float
    spread: float
    profit_estimate: str