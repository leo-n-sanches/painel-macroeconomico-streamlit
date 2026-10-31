# %%

import os

import dotenv
import pandas as pd
import pyarrow
import requests
import sqlalchemy

dotenv.load_dotenv()

# %%

BRAPI_TOKEN = os.getenv("BRAPI_TOKEN")

path_storage = "../storage"

engine = sqlalchemy.create_engine("sqlite:///test.db")

extract_list = [
    "PETR4",
    "ITUB4",
    "VALE3",
    "ABEV3",
    "EMBJ3",
    "BTC"
]

url = f"https://brapi.dev/api/v2/stocks/quote?symbols=BTC&token={BRAPI_TOKEN}"
resp = requests.get(url)
response = resp.json()

print(response)

# %%

colunas = [
    "data.shortName",
    "data.regularMarketPreviousClose",
    "data.regularMarketPrice",
    "data.regularMarketDayHigh",
    "data.regularMarketDayLow",
    "data.regularMarketDayRange",
    "data.regularMarketChange",
    "data.regularMarketChangePercent",
    "data.regularMarketTime"
]

colunas_novas = [
    "name",
    "marketprice",
    "marketdayhigh",
    "marketdaylow",
    "marketdayrange",
    "marketchange",
    "marketchangepercent",
    "time",
    "marketpreviousprice"
]

# %%

df = pd.json_normalize(response["results"])[colunas]

# df

df = df.to_parquet()

# %%

