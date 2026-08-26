
from fastapi import FastAPI
from pydantic import BaseModel
from settings import ScannerSettings
from services import build_arbitrage_scanner


app = FastAPI(title="Arbitrage Scanner")

class ScanRequest(BaseModel):
    capital: float
    currency: str
print("-3. Before build arbitrage scanner")
arbitrage = build_arbitrage_scanner()
print("-2. . After build arbitrage scanner")
@app.post("/arbitrage/scan")

def scan(request: ScanRequest):
    print("-1. In scan func in api")
    settings = ScannerSettings(
        capital=request.capital,
        currency=request.currency
    )
    print("0. Before arbitrage search in api")
    result =  arbitrage.search(settings)
    print("7. Search returned")
    return result
###################################################
