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

path_storage = "./storage/"

extract_list = [
    "PETR4",
    "ITUB4",
    "VALE3",
    "ABEV3",
    "EMBJ3",
    "BTC"
]

colunas_novas = {
    "symbol" : "symbol",
    "data.longName" : "name",
    "data.regularMarketPreviousClose" : "marketprice",
    "data.regularMarketPrice" : "marketdayhigh",
    "data.regularMarketDayHigh" : "marketdaylow",
    "data.regularMarketDayLow" : "marketdayrange",
    "data.regularMarketDayRange" : "marketchange",
    "data.regularMarketChange" : "marketchangepercent",
    "data.regularMarketChangePercent" : "time",
    "data.regularMarketTime" : "marketpreviousprice",
}

colunas = [
    "symbol",
    "name",
    "marketprice",
    "marketdayhigh",
    "marketdaylow",
    "marketdayrange",
    "marketchange",
    "marketchangepercent",
    "time",
    "marketpreviousprice",
]

# %%

def teste(extract_list, BRAPI_TOKEN):

    urls = []

    for i in extract_list:
        url = f"https://brapi.dev/api/v2/stocks/quote?symbols={i}&token={BRAPI_TOKEN}"
        urls.append(url)

    return urls

urls = teste(extract_list, BRAPI_TOKEN)

# %%

resp = requests.get(urls)
response = resp.json()
df = pd.json_normalize(response["results"])[colunas]

# %%

def teste2(urls):

    lista_df = []

    for url in urls:
        resp = requests.get(url)
        response = resp.json()
        df_temp = pd.json_normalize(response["results"])
        df_temp = df_temp.rename(columns=colunas_novas)[colunas]
        lista_df.append(df_temp)
        
    return lista_df

lista_df = teste2(urls)

# %%

for i, df in zip(extract_list, lista_df):
    df.to_parquet(path=f"{path_storage}{i}_daily.parquet", index=False)



