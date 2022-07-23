import requests 
import pandas as pd
import json
from datetime import datetime
import itertools


if __name__ == "__main__":
    df_path = r"examples\results\BTCUSD_with_no_int\0\position.csv"
    df = pd.read_csv(df_path,index_col=0)
    del df["datetime"]
    df["interaction"] = [df.loc[index].values.all() for index in df.index]
    df["union"] = [df.loc[index].values.any() for index in df.index]
    df.to_csv(r"position.csv")
