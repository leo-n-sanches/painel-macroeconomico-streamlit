# %%

import os
from datetime import datetime, timezone

import boto3
import dotenv
import pandas as pd
import requests
from botocore.exceptions import ClientError

dotenv.load_dotenv()

# %%

S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")

s3_route_bcb = "painel_macro/cdc/bcb/"
path_storage_bcb = "./storage/bcb/cdc/"

moeda = [
    "USD",
    "EUR"
]

moeda_save = [
    "dolar",
    "euro"
]

colunas = [
    "cotacaoCompra",
    "cotacaoVenda",
    "dataHoraCotacao",
    "tipoBoletim"
]

# %%

class Bcb_Ptax_Pipeline:
    def __init__(self, 
                 S3_BUCKET: str, 
                 s3_route_bcb: str, 
                 path_storage_bcb: str, 
                 S3_REGION: str
                 ):
        self.S3_BUCKET = S3_BUCKET
        self.s3_route_bcb = s3_route_bcb
        self.path_storage_bcb = path_storage_bcb
        self.time_now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        # self.data_ptax = datetime.now(timezone.utc).strftime("%m-%d-%Y")
        self.data_ptax = "11-22-2026"
        self.s3_client = boto3.client("s3", region_name=S3_REGION)
        
        self.MAX_ARQUIVOS = 5
        self.contador = 0

    def extract_urls(self, moeda: list[str]) -> list:

        urls = []

        for i in moeda:
            url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=%27{i}%27&@dataCotacao=%27{self.data_ptax}%27&$format=json"
            urls.append(url)

        return urls

    def list_dfs(self, urls: list[str]) -> list:
    
            df_list = []
    
            for url in urls:
                resp = requests.get(url)
                response = resp.json()

                if not response.get('value'):
                    print("No data - Weekend")
                    continue

                df_temp = pd.json_normalize(response, record_path=['value'])[colunas]
                df_list.append(df_temp)
                
            return df_list

    def save_files(self, moeda_save: list[str], df_list: list[str]):

        contador = 0

        for i, df in zip(moeda_save, df_list):

            if contador >= self.MAX_ARQUIVOS:
                    print("Limite de segurança de carga do s3 ativado")
                    break

            contador = contador + 1

            file_name = f"{i}/{i}_{self.time_now}.parquet"
            file_path = f"{self.path_storage_bcb}{file_name}"
            route_path = f"{self.s3_route_bcb}{file_name}"

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
    
    def exec_all_bcb(self, moeda: list[str], moeda_save: list[str]):
            resultado = self.extract_urls(moeda=moeda)
            df_list = self.list_dfs(urls=resultado)

            if not df_list:
                 return

            self.save_files(moeda_save=moeda_save, df_list=df_list)


# %%

# pipeline = Bcb_Ptax_Pipeline(
#     S3_BUCKET=S3_BUCKET,
#     s3_route_bcb=s3_route_bcb,
#     path_storage_bcb=path_storage_bcb,
#     S3_REGION=S3_REGION
#     )

# pipeline.exec_all_bcb(moeda=moeda, moeda_save=moeda_save)
