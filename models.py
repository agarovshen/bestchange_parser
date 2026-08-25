class ExchangeDirection:
    def __init__(self, rates, direction_data):
        self.rates = rates
        self.direction_id = direction_data["direction_id"]
        self.from_currency_code = direction_data["from_currency_code"]
        self.to_currency_code = direction_data["to_currency_code"]
        self.from_currency_id = direction_data["from_currency_id"]
        self.to_currency_id = direction_data["to_currency_id"]
    ###############################################################
    def with_rates(self, rates):
        return ExchangeDirection(self.from_currency, self.to_currency, rates)
    def __str__(self):
        return f"{self.from_currency_code} -> {self.to_currency_code}"
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
        self.id_by_code = {
            currency.code: currency
            for currency in self.currencies
        }
        self.code_by_id = {
            currency.currency_id: currency
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
            changer.changer_id: changer.name
            for changer in self.changers
        }
    
class Rate:
    def __init__(self, rate):
        self.rate = float(rate["rate"])
        self.direction_id = rate["direction_id"]
        self.changer = rate["changer"]
        self.inmin = rate["inmin"]


class Rates:
    def __init__(self, rates):
        self.rate_objects = []
        for rate in rates:
            self.rate_objects.append(Rate(rate))
    ##############################################################
    def select_cheapest(self, top=2):      
        return sorted(self.rate_objects, key=lambda r: r.rate)[:top]
    ###############################################################
    def select_best(self, top=2):
        return sorted(self.rate_objects, key=lambda r: r.rate, reverse=True)[:top]