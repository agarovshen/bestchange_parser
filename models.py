class ExchangeDirection:
    def __init__(self, from_currency, to_currency, rates):
        self.from_currency = from_currency
        self.to_currency = to_currency
        self.rates = rates
    ###############################################################
    def with_rates(self, rates):
        return ExchangeDirection(self.from_currency, self.to_currency, rates)
    def __str__(self):
        return f"{self.from_currency.code} -> {self.to_currency.code}"
    
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
    def __init__(self, data):
        self.rate = float(data["rate"])
        self.inmin = data["inmin"]
    def normalize_rate(self):
        if self.rate < 0.01:
            self.exchange_rate = 1/self.rate
        else:
            self.exchange_rate = self.rate

class Rates:
    def __init__(self, data):
        self.rates = []
        for r in data:
            self.rates.append(Rate(r))
    ##############################################################
    def select_cheapest(self, top=2):      
        return sorted(self.rates, key=lambda r: r.rate)[:top]
    ###############################################################
    def select_best(self, top=2):
        return sorted(self.rates, key=lambda r: r.rate, reverse=True)[:top]