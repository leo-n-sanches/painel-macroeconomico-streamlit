# %%

import os
import dotenv
import pandas as pd
import pyarrow
import requests
import boto3

dotenv.load_dotenv()

BRAPI_TOKEN = os.getenv("BRAPI_TOKEN")

path_storage = "./storage/brapi/full_load/"
data_range = "&interval=1d&range=3mo"

BRAPI_TOKEN = os.getenv("BRAPI_TOKEN")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")
s3_route = "painel_macro/full_load/brapi/"

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
    "volume",
    "close",
    "low",
    "high",
    "open",
    "date"
]

colunas_novas = {
    "results.symbol": "symbol",
    "volume": "volume",
    "close": "close",
    "low": "low",
    "high": "high",
    "open": "open",
    "date": "date"
}

# %%

def teste(BRAPI_TOKEN, data_range, extract_list):

    urls = []

    for i in extract_list:
        url = f"https://brapi.dev/api/v2/stocks/historical?symbols={i}{data_range}&token={BRAPI_TOKEN}"
        urls.append(url)

    return urls

urls = teste(BRAPI_TOKEN, data_range, extract_list)

# %%

def teste2(urls):

    lista_dfs = []

    for url in urls:

        resp = requests.get(url)
        response = resp.json()
        df_temp = pd.json_normalize(response, 
                            record_path=['results', 'data', 'historicalDataPrice'],
                            meta=[['results', 'symbol']]
                            )
        df_temp = df_temp.rename(columns=colunas_novas)[colunas]
        lista_dfs.append(df_temp)

    return lista_dfs

lista_dfs = teste2(urls)

# %%

for i, df in zip(extract_list, lista_dfs):
    df.to_parquet(path=f"{path_storage}{i}_full_load.parquet", index=False)
