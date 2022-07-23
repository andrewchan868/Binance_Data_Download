import requests 
import pandas as pd
import json
from datetime import datetime
import itertools

if __name__ == "__main__":
    symbols = [["BTC","ETH","BNB","ADA","DOGE","XRP","DOT","LTC"],["USDT"],[""]] # "_210625","_210326"
    symbols = [ x[0]+x[1]+x[2] for x in list(itertools.product(*symbols))]
    
    base_url = "https://fapi.binance.com" 
    for symbol in symbols:
        print(symbol)
        startTime = 1432195623000
        data = []
        try:
            while True:
                data_url = f"{base_url}/fapi/v1/fundingRate?symbol={symbol}&limit=1000" + f"&startTime={startTime}"
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
        except Exception as e:
            print("error",e)