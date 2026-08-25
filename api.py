import requests
from config import API_KEY
from fastapi import FastAPI
from pydantic import BaseModel
from settings import ScannerSettings
from services import build_arbitrage_scanner

BASE_URL = "https://bestchange.app/v2"

app = FastAPI(title="Arbitrage Scanner")
# @app.get("/")
# def root():
#     return {"message": "Arbitrage Scanner"}

class ScanRequest(BaseModel):
    capital: float
    currency: str

@app.post("/arbitrage/scan")

def scan(request: ScanRequest):
    setting = ScannerSettings(
        capital=request.capital,
        currency=request.currency
    )
    return{
        "pul": setting.capital,
        "walyuta": setting.currency
    }
###################################################
def get_data(data_type):
    url = f"{BASE_URL}/{API_KEY}/{data_type}/en"
    response = requests.get(url)
    data = response.json()
    return data.get(data_type, [])
###################################################
def load_rates(paths):
    url = f"{BASE_URL}/{API_KEY}/rates/{paths}"
    response = requests.get(url)
    data = response.json()
    rates_dict = data.get("rates", {})
    return rates_dict
####################################################