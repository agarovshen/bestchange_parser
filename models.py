class ExchangeDirection:
    def __init__(self, from_code, to_code, rates):
        self.from_code = from_code
        self.to_code = to_code
        self.rates = rates
        self.spreads = []

    def __str__(self):
        return f"{self.from_code} -> {self.to_code}"