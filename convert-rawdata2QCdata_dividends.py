import requests 
import pandas as pd
import json
from datetime import datetime,timedelta

if __name__ == "__main__":
    symbols = ["BTC","ETH","BNB","ADA","DOGE","XRP","DOT","LTC"]
    for symbol in symbols:
        url = symbol + "USDT_prep_funding_rate.csv"
        columns = ["Day","fundingRate"]
        df = pd.read_csv(url)
        df = df[columns]
        df = df.rename(columns={'Day': 'date',"Open":"open", "High":"high", "Low":"low", "Close":"close","fundingRate":"dividend"})
        df["dividend"] = -1*df["dividend"]
        df["date"] = pd.to_datetime(df["date"])
        df.to_csv("QC_"+symbol + "USDT_prep.csv", index=False)

