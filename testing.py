import requests 
import pandas as pd
import json
from datetime import datetime
import itertools
import ccxt

if __name__ == "__main__":
    exchange = ccxt.ftx({'verbose': True})
    securities = pd.DataFrame(exchange.load_markets(True)).transpose()
    securities.to_csv("securities.csv")