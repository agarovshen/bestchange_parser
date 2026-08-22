from dataclasses import dataclass

@dataclass
class ScannerSettings:
    capital: float = 1000
    currency: str = "USDTBEP20"
