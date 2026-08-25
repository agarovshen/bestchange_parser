from repository import ExchangeRepository
from arbitrage import ArbitrageScanner


def build_arbitrage_scanner():
    repository = ExchangeRepository()
    return ArbitrageScanner(repository)