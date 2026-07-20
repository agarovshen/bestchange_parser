import requests
from config import API_KEY
BASE_URL = "https://bestchange.app/v2"
###################################################
def get_data(data_type):
    url = f"{BASE_URL}/{API_KEY}/{data_type}/en"
    response = requests.get(url)
    data = response.json()
    return data.get(data_type, [])
###################################################
def load_rates(from_id, to_id):
    url = f"{BASE_URL}/{API_KEY}/rates/{from_id}-{to_id}"
    response = requests.get(url)
    data = response.json()
    rates_dict = data.get("rates", {})
    rates = list(rates_dict.values())[0]
    return rates