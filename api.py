from locale import currency

from fastapi import FastAPI
from pydantic import BaseModel
from settings import ScannerSettings
from services import build_arbitrage_scanner


app = FastAPI(title="Arbitrage Scanner")

class ScanRequest(BaseModel):
    capital: float=100
    currency: str="USDTBEP20"
arbitrage = build_arbitrage_scanner()
@app.post("/arbitrage/scan")

def scan(request: ScanRequest):
    settings = ScannerSettings(
        capital=request.capital,
        currency=request.currency
        )
    result =  arbitrage.search(settings)
    return {
        "count": len(result),
        "results": result
        }
###################################################