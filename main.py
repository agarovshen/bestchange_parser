from gui import run_app
from repository import ExchangeRepository
from models import Changers, Currencies
from arbitrage import ArbitrageScanner

def build_service():
    repository = ExchangeRepository()
    changers_data = repository.get_changers()
    currencies_data = repository.get_currencies()
    changers = Changers(changers_data)
    currencies = Currencies(currencies_data)
    return ArbitrageScanner(changers, currencies, repository)

def main():
    arbitrage = build_service()
    run_app(arbitrage.search)
main()