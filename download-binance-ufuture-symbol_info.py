import requests 
import pandas as pd
import json
from datetime import datetime
import itertools

if __name__ == "__main__":
    #base_url = "https://fapi.binance.com" 
    #base_url = "https://dapi.binance.com" 
    base_url = "https://api.binance.com" 
    #data_url = f"{base_url}/fapi/v1/exchangeInfo"
    #data_url = f"{base_url}/dapi/v1/exchangeInfo"
    data_url = f"{base_url}/api/v1/exchangeInfo"
    res = requests.get(url=data_url)
    results = json.loads(res.text)["symbols"]
    temp_results = [{k:v for k,v in res.items() if type(v)!=list} for res in results]
    data_df = pd.DataFrame(temp_results)
    #data_df["deliveryDate"] = [datetime.utcfromtimestamp(x/1000) for x in list(data_df["deliveryDate"].values) ]
    #data_df["onboardDate"] = [datetime.utcfromtimestamp(x/1000) for x in list(data_df["onboardDate"].values) ]
    data_df = data_df.to_csv("spot_symbol_info.csv")