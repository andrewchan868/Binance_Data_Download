import requests 
import pandas as pd
import json
from datetime import datetime

if __name__ == "__main__":
    symbols = ["BTCUSDT","ETHUSDT","BNBUSDT","ADAUSDT","DOGEUSDT","XRPUSDT","DOTUSDT","LTCUSDT"]
    symbols = symbols + [ s + "_prep" for s in symbols]
    for symbol in symbols:
        url = symbol + ".csv"
        columns = ["Day","Open","High","Low","Close"]
        df = pd.read_csv(url)
        df = df[columns]
        df = df.rename(columns={'Day': 'date',"Open":"open", "High":"high", "Low":"low", "Close":"close"})
        df["date"] = pd.to_datetime(df["date"])
        df.to_csv("QC_"+url, index=False)

