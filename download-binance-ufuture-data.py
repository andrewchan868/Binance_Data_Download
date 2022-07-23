import requests 
import pandas as pd
import json
from datetime import datetime
import itertools

if __name__ == "__main__":
    base_url = "https://fapi.binance.com" 

    symbols = [["BTC","ETH","BNB","ADA","DOGE","XRP","DOT","LTC"],["USDT"],[""]] # "_210625","_210326"
    symbols = [ x[0]+x[1]+x[2] for x in list(itertools.product(*symbols))]
    columns = ["Open time","Open","High","Low","Close","Volume","Close time","Quote asset volume","Number of trades","Taker buy base asset volume","Taker buy quote asset volume","Ignore"]
    
    for symbol in symbols:
        startTime = 1432195623000
        data = []
        print(symbol)
        while True:
            data_url = f"{base_url}/fapi/v1/klines?symbol={symbol}&limit=1000&interval=1h" + f"&startTime={startTime}"
            res = requests.get(url=data_url)
            temp_data = json.loads(res.text)
            if len(temp_data) == 0:
                break
            data.extend(temp_data)
            startTime = int(temp_data[-1][0]) + 1
        df = pd.DataFrame(data,columns= columns)
        df["Day"] = [datetime.utcfromtimestamp(x/1000) for x in list(df["Open time"].values) ]
        temp_columns = columns.copy()
        temp_columns.insert(1,"Day")
        df = df[temp_columns]
        df.to_csv(f"{symbol}_prep.csv",index=False)