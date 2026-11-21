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

BRAPI_TOKEN = os.getenv("BRAPI_TOKEN")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")
s3_route = "painel_macro/cdc/brapi/"

path_storage = "./storage/brapi/cdc/"

extract_list = [
    "PETR4",
    "ITUB4",
    "VALE3",
    "ABEV3",
    "EMBJ3",
    "BTC"
]

extract_list_small = [p.lower() for p in extract_list]

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

class Brapi_S3_Pipeline_cdc:
    def __init__(self, 
                 S3_BUCKET: str, 
                 s3_route: str, 
                 path_storage: str, 
                 S3_REGION: str, 
                 BRAPI_TOKEN: str
                 ):
        self.S3_BUCKET = S3_BUCKET
        self.s3_route = s3_route
        self.path_storage = path_storage
        self.time_now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.s3_client = boto3.client("s3", region_name=S3_REGION)
        self.BRAPI_TOKEN = BRAPI_TOKEN
        
        self.MAX_ARQUIVOS = 10
        self.contador = 0

    def extract_urls(self, extract_list: list[str]) -> list:

        urls = []

        for i in extract_list:
            url = f"https://brapi.dev/api/v2/stocks/quote?symbols={i}&token={self.BRAPI_TOKEN}"
            urls.append(url)

        return urls

    def list_dfs(self, urls: list[str]) -> list:

        df_list = []

        for url in urls:
            resp = requests.get(url)
            response = resp.json()
            df_temp = pd.json_normalize(response["results"])
            df_temp = df_temp.rename(columns=colunas_novas)[colunas]
            df_list.append(df_temp)
            
        return df_list

    def save_files(self, extract_list_small: list[str], df_list: list[str]):

        contador = 0

        for i, df in zip(extract_list_small, df_list):

            if contador >= self.MAX_ARQUIVOS:
                    print("Limite de segurança de carga do s3 ativado")
                    break

            contador = contador + 1

            file_name = f"{i}/{i}_{self.time_now}.parquet"
            file_path = f"{path_storage}{file_name}"
            route_path = f"{s3_route}{file_name}"

            df.to_parquet(path=file_path, index=False)

            try:
                self.s3_client.upload_file(
                    Filename=file_path,
                    Bucket=self.S3_BUCKET,
                    Key=route_path
                )
                print(f"Enviado {file_name}. Arquivo {contador} | Limite {self.MAX_ARQUIVOS}")

            except ClientError as erro:
                print(f"Erro ao enviar {file_name}: {erro}")

    def exec_all(self, extract_list: list[str], extract_list_small: list[str]):
        resultado = self.extract_urls(extract_list=extract_list)
        df_list = self.list_dfs(urls=resultado)
        self.save_files(extract_list_small=extract_list_small, df_list=df_list)

# %%

pipeline = Brapi_S3_Pipeline_cdc(
    S3_BUCKET=S3_BUCKET,
    s3_route=s3_route,
    path_storage=path_storage,
    S3_REGION=S3_REGION,
    BRAPI_TOKEN=BRAPI_TOKEN
    )

# pipeline.exec_all(extract_list=extract_list, extract_list_small=extract_list_small)
