import requests 
import pandas as pd
import json
from datetime import datetime

if __name__ == "__main__":
    base_url = "https://dapi.binance.com" 
    symbols = ["BTCUSD_PERP","ETHUSD_PERP"]
    
    for symbol in symbols:
        startTime = 1432195623000
        data = []
        while True:
            data_url = f"{base_url}/dapi/v1/fundingRate?symbol={symbol}&limit=1000" + f"&startTime={startTime}"
            res = requests.get(url=data_url)
            temp_data = json.loads(res.text)
            if len(temp_data) == 0:
                break
            data.extend(temp_data)
            startTime = temp_data[-1]["fundingTime"] + 1
        df = pd.DataFrame(data)
        df["fundingTime"] = [int(x/1000)*1000 for x in list(df["fundingTime"].values) ]
        df["Day"] = [datetime.utcfromtimestamp(x/1000) for x in list(df["fundingTime"].values) ]
        df.to_csv(f"{symbol}_prep_funding_rate.csv",index=False)
        print(symbol)