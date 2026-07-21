class ExchangeDirection:
    def __init__(self, from_currency, to_currency, rates):
        self.from_code = from_currency.code
        self.to_code = to_currency.code
        self.rates = rates
        self.use_reverse_spread = False
        self.spreads = []
        self.selected_rates = []
    ###############################################################
    def select_cheapest(self, top=2):      
        self.rates.sort(key=lambda r: r["exchange_rate"])
        self.selected_rates = self.rates[:top]
        return self.selected_rates
    ###############################################################
    def select_best(self, top=2):
        self.rates.sort(key=lambda r: r["exchange_rate"], reverse=True)
        self.selected_rates = self.rates[:top]
        return self.rates[:top]
    ###############################################################
    def __str__(self):
        return f"{self.from_code} -> {self.to_code}"
    
class Currency:
    def __init__(self, name, code, currency_id):
        self.name = name
        self.code = code
        self.currency_id = currency_id

class Currencies:
    def __init__(self, data):
        self.currencies = []
        for d in data:
            self.currencies.append(Currency(
                name = d["name"],
                code = d["code"],
                currency_id = d["id"]
            ))
    def get_by_code(self, code):
        for currency in self.currencies:
            if code == currency.code:
                return currency
        print("Currency not found")
        return None
    
class Changers:
    def __init__(self):
        pass