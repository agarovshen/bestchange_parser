import requests


FAST_API_URL = "http://127.0.0.1:8000"

def scan_arbitrage(settings, directions_var = 2):
    url = f"{FAST_API_URL}/arbitrage/scan"
    payload = {
        "capital": settings.capital,
        "currency": settings.currency
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    data = response.json()
    return data.get("results", [])