from api import get_data
from gui import run_app
from database import Database
from services import ExchangeServices
from models import Changers, Currencies

def build_service():       
    changers_data = get_data("changers")
    currencies_data = get_data("currencies")
    changers = Changers(changers_data)
    currencies = Currencies(currencies_data)
    return ExchangeServices(changers, currencies)

def main():
    services = build_service()
    run_app(services.search)
main()