import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

COINMARKETCAP_APIKEY = os.getenv("COINMARKETCAP_APIKEY")

headers = {'Accept': 'application/json',
           'Accept-Encoding': 'deflate, gzip',
           'X-CMC_PRO_API_KEY': COINMARKETCAP_APIKEY}


def get_price(slug, headers=headers):
    """Getting price in USD"""
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest?slug={slug}&convert=USD'
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        r_json = json.loads(r.text)
        currency_id = list(r_json['data'])[0]
        price = r_json['data'][currency_id]['quote']['USD']['price']
        return round(price, 2)
    else:
        return 'Something went wrong\nTry again'
