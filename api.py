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

changers = get_data("changers")

def get_changers_map(changers):
    changers_map = {
        changer["id"] : changer["name"] 
        for changer in changers
    }
    return changers_map
changers_map = get_changers_map(changers)
###################################################
def load_rates(from_id, to_id):
    url = f"{BASE_URL}/{API_KEY}/rates/{from_id}-{to_id}"
    response = requests.get(url)
    data = response.json()
    rates_dict = data.get("rates", {})
    rates = list(rates_dict.values())[0]
    # print(rates, type(rates))
    changers_map = get_changers_map(changers)
    for r in rates:
        r["changer_name"] = changers_map[r["changer"]]
    return rates
###################################################
def get_rates(from_code, to_code, use_reverse_spread=False):
    from_id = get_currency_id(currencies, from_code)
    to_id = get_currency_id(currencies, to_code)
    if not from_id or not to_id:
        print("Currency not found")
        return [], []
    direct_rates = load_rates(from_id, to_id)
    reverse_rates = []
    if use_reverse_spread:
        reverse_rates = load_rates(to_id, from_id)
    return direct_rates, reverse_rates
##################################################

currencies = get_data("currencies")
def get_currency_id(currencies, code):
    for c in currencies:
        if c["code"] == code:
            return c["id"]
    return None
