from dataclasses import dataclass

@dataclass
class ScannerSettings:
    capital: float = 1000,
    min_profit: float = 5,
    check_inmin: bool = True,
