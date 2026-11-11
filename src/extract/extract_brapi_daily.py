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

path_storage = "./storage/teste"

engine = sqlalchemy.create_engine("sqlite:///test.db")

extract_list = [
    "PETR4",
    "ITUB4",
    "VALE3",
    "ABEV3",
    "EMBJ3",
    "BTC"
]

colunas = [
    "symbol",
    "data.longName",
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
    "symbol",
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
url = f"https://brapi.dev/api/v2/stocks/quote?symbols=PETR4&token={BRAPI_TOKEN}"
resp = requests.get(url)
response = resp.json()

print(response)

# %%

df = pd.json_normalize(response["results"])
# df = pd.json_normalize(response["results"])[colunas]

df

# %%

df = df.to_parquet(path=f"{path_storage}.parquet")
# df = df.to_csv(f"{path_storage}.csv", sep=";")

# %%
