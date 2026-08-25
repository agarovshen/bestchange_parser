from gui import run_app
from services import build_arbitrage_scanner



def main():
    arbitrage = build_arbitrage_scanner()
    run_app(arbitrage.search)
main()