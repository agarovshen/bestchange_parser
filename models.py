class ExchangeDirection:
    def __init__(self, from_code, to_code, rates):
        self.from_code = from_code
        self.to_code = to_code
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