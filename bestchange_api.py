import requests
from config import API_KEY
BASE_URL = "https://bestchange.app/v2"

def fetch_data(data_type):
    url = f"{BASE_URL}/{API_KEY}/{data_type}/en"
    response = requests.get(url)
    data = response.json()
    return data.get(data_type, [])
###################################################
def fetch_rates(paths):
    url = f"{BASE_URL}/{API_KEY}/rates/{paths}"
    response = requests.get(url)
    data = response.json()
    rates_dict = data.get("rates", {})
    return rates_dict
####################################################