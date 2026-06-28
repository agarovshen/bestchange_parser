import requests
from config import API_KEY
BASE_URL = "https://bestchange.app/v2"
###################################################
def get_currencies():
    url = f"{BASE_URL}/{API_KEY}/currencies/en"
    response = requests.get(url)
    data = response.json()
    return data.get("currencies", [])
###################################################
def get_rates(from_id, to_id):
    url = f"{BASE_URL}/{API_KEY}/rates/{from_id}-{to_id}"
    response = requests.get(url)
    data = response.json()
    return data.get("rates", {})
get_rates(48,93)