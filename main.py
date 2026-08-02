from gui import run_app
from repository import ExchangeRepository
from services import ExchangeServices
from models import Changers, Currencies

def build_service():
    repository = ExchangeRepository()
    changers_data = repository.get_changers()
    currencies_data = repository.get_currencies()
    changers = Changers(changers_data)
    currencies = Currencies(currencies_data)
    return ExchangeServices(changers, currencies, repository)

def main():
    services = build_service()
    run_app(services.search)
main()