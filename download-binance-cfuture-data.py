import requests 
import pandas as pd
import json
from datetime import datetime
import itertools

if __name__ == "__main__":
    base_url = "https://dapi.binance.com" 
    symbols = [["BTC","ETH"],["USD"],["_PERP","_200925","_201225","_210326","_210625","_210924"]]
    symbols = [ x[0]+x[1]+x[2] for x in list(itertools.product(*symbols))]
    columns = ["Open time","Open","High","Low","Close","Volume","Close time","Quote asset volume","Number of trades","Taker buy base asset volume","Taker buy quote asset volume","Ignore"]
    for symbol in symbols:
        endTime = None
        data = []
        while True:
            data_url = f"{base_url}/dapi/v1/klines?symbol={symbol}&limit=1500&interval=1h"
            if endTime:
                data_url += f"&endTime={endTime}"
            res = requests.get(url=data_url)
            temp_data = json.loads(res.text) 
            if len(temp_data) == 0:
                break
            data.extend(temp_data)
            endTime = int(temp_data[0][0]) - 1
        df = pd.DataFrame(data,columns= columns)
        df["Day"] = [datetime.utcfromtimestamp(x/1000) for x in list(df["Open time"].values) ]
        temp_columns = columns.copy()
        temp_columns.insert(1,"Day")
        df = df[temp_columns]
        df.sort_values(by=["Open time"],inplace = True)
        df.to_csv(f"{symbol}.csv",index=False)
        print(symbol)