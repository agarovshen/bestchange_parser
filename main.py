from gui import run_app
from repository import ExchangeRepository
from arbitrage import ArbitrageScanner

def build_service():
    repository = ExchangeRepository()
    return ArbitrageScanner(repository)

def main():
    arbitrage = build_service()
    run_app(arbitrage.search)
main()