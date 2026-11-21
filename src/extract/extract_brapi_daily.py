# %%

import os
from datetime import datetime, timezone

import boto3
import dotenv
import pandas as pd
import pyarrow
import requests
from botocore.exceptions import ClientError

dotenv.load_dotenv()

# %%

BRAPI_TOKEN = os.getenv("BRAPI_TOKEN")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")
s3_route = "painel_macro/cdc/brapi/"

s3_client = boto3.client("s3", region_name=S3_REGION)

time_now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

path_storage = "./storage/brapi/cdc/"

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

extract_list_small = [p.lower() for p in extract_list]

# file_name = f"{i}/{i}_{time_now}.parquet"
# file_path = f"{path_storage}{file_name}"
# route_path = f"{s3_route}{file_name}"

# for i, df in zip(extract_list_small, lista_df):
#     df.to_parquet(path=file_path, index=False)

# print(route_path)

# %%

MAX_ARQUIVOS = 10
contador = 0

for i, df in zip(extract_list_small, lista_df):

    if contador >= MAX_ARQUIVOS:
            print("Limite de segurança de carga do s3 ativado")
            break

    contador += 1

    file_name = f"{i}/{i}_{time_now}.parquet"
    file_path = f"{path_storage}{file_name}"
    route_path = f"{s3_route}{file_name}"

    df.to_parquet(path=file_path, index=False)

    try:
        s3_client.upload_file(
            Filename=file_path,
            Bucket=S3_BUCKET,
            Key=route_path
        )
        print(f"Enviado {file_name}")

    except ClientError as erro:
        print(f"Erro ao enviar {file_name}: {erro}")

# %%
