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
def get_changers():
    url = f"{BASE_URL}/{API_KEY}/changers/en"
    response = requests.get(url)
    data = response.json()
    return data.get("changers", [])
def get_changers_map(changers):
    changers_map = {
        changer["id"] : changer["name"] 
        for changer in changers
    }
    return changers_map
###################################################
def get_rates(from_id, to_id):
    url = f"{BASE_URL}/{API_KEY}/rates/{from_id}-{to_id}"
    response = requests.get(url)
    data = response.json()
    rates_dict = data.get("rates", {})
    rates = list(rates_dict.values())[0]
    for r in rates:
        name = changers_map.get(r["changer"])
        r["changer_name"] = name
    return rates
##################################################
currencies = get_currencies()
changers = get_changers()
changers_map = get_changers_map(changers)
##################################################

##################################################
def get_currency_id(currencies, code):
    for c in currencies:
        if c["code"] == code:
            return c["id"]
    return None
##################################################
def get_rates_by_name(from_code, to_code):
    from_id = get_currency_id(currencies,from_code)
    to_id = get_currency_id(currencies, to_code)
    if not from_id or not to_id:
        print("Currency not found")
        return[]
    rates = get_rates(from_id, to_id)
    return rates