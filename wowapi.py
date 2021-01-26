import requests
import json
import numpy as np
import pandas as pd


# Create OAuth access token from client id and client secret
def create_access_token(client_id, client_secret, region='us'):
    data = {'grant_type': 'client_credentials'}
    response = requests.post('https://%s.battle.net/oauth/token' % region, data=data, auth=(client_id, client_secret))

    return response.json()


# Retrieve auctions. Inputs: URL and access token, concatenated
def retrieve_auctions(token):
    if not token['access_token']:
        print('Invalid token')
        return

    auctions = requests.get('https://us.api.blizzard.com/data/wow/connected-realm/1427/'
                            'auctions?namespace=dynamic-us&locale=en_US&access_token={}'
                            .format(token['access_token']))
    return auctions.json()


def clean_data(data):
    # (1) extracts item id from embedded list; (2) fills in empty unit prices
    # (3) drops buyout and bid columns; (4) adds timestamp
    base_frame = pd.DataFrame(data["auctions"])
    embedded_frame = [0]*len(base_frame)
    empty_prices = [0] * len(base_frame)

    for i in (range(len(base_frame))):
        embedded_frame[i] = base_frame["item"][i]["id"]
        empty_prices[i] = base_frame["buyout"][i] / base_frame["quantity"][i]
    base_frame["item"] = embedded_frame

    # fill in empty unit prices
    base_frame["unit_price"] = pd.to_numeric(base_frame["unit_price"], errors='coerce')
    base_frame["unit_price"] = base_frame["unit_price"].fillna(0)
    empty_prices = pd.Series(empty_prices).fillna(0).tolist()
    base_frame["unit_price"] = base_frame["unit_price"]+empty_prices

    # (3) drop columns
    base_frame = base_frame.drop(columns=["buyout","bid"])

    # (4) insert timestamp
    base_frame.insert(0, 'TimeStamp', pd.to_datetime('now').replace(microsecond=0))

    return base_frame