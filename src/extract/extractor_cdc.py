# %%

import os
from datetime import datetime, timezone

import boto3
import dotenv
import requests
from botocore.exceptions import ClientError
from alpha_cdc import (
    name_list_alpha,
    path_storage_alpha,
    s3_route_alpha,
    urls_alpha,
)
from bcb_cdc import (
    name_list_bcb,
    path_storage_bcb,
    s3_route_bcb,
    urls_bcb,
)
from bcb_ptax_cdc import (
    name_list_ptax,
    path_storage_ptax,
    s3_route_ptax,
    urls_ptax,
)
from brapi_cdc import (
    name_list_brapi,
    path_storage_brapi,
    s3_route_brapi,
    urls_brapi,
)
from frank_cdc import (
    name_list_frank,
    path_storage_frank,
    s3_route_frank,
    urls_frank,
)

dotenv.load_dotenv()

S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")

all_url = [urls_brapi, 
           urls_frank, 
           urls_ptax, 
           urls_bcb, 
           urls_alpha]
all_lists = [name_list_brapi, 
             name_list_frank, 
             name_list_ptax, 
             name_list_bcb, 
             name_list_alpha]
all_path_storage = [path_storage_brapi, 
                    path_storage_frank, 
                    path_storage_ptax, 
                    path_storage_bcb, 
                    path_storage_alpha]
all_s3_route = [s3_route_brapi, 
                s3_route_frank, 
                s3_route_ptax, 
                s3_route_bcb, 
                s3_route_alpha]

# %%
class Brapi_S3_Pipeline_Cdc:
    def __init__(self, 
                 S3_BUCKET: str, 
                 S3_REGION: str, 
                 all_url: list[list[str]],
                 all_lists: list[list[str]],
                 all_path_storage: list[list[str]],
                 all_s3_route: list[list[str]]
                 ):
        self.S3_BUCKET = S3_BUCKET
        self.time_now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.s3_client = boto3.client("s3", region_name=S3_REGION)
        self.all_url = all_url
        self.all_lists = all_lists
        self.all_path_storage = all_path_storage
        self.all_s3_route = all_s3_route
        
        self.MAX_ARCHIVES = 10
        self.counter = 0

    def write_json(self) -> list:

        for url_list, name_list, path_list in zip(self.all_url, self.all_lists, self.all_path_storage):

            path = path_list[0]

            for url, name in zip(url_list, name_list):
                resp = requests.get(url)
                dados = resp.json()

                if any(chave in dados for chave in ("Information", "Note", "Error Message")):
                    print(f"Limite atingido para API na extração de {name}")
                    continue

                if "value" in dados and len(dados["value"]) == 0:
                    print(f"Sem dados disponíveis para {name} hoje (fim de semana/feriado).")
                    continue

                with open(path + f"{name}/{name}_{self.time_now}.json", "wb") as arquivo:
                    arquivo.write(resp.content)
            
    def save_files(self):

        for  name_list, path_list, route_list in zip(self.all_lists, self.all_path_storage, self.all_s3_route):

            path = path_list[0]
            route = route_list[0]
            counter = 0

            for name in name_list:

                if counter >= self.MAX_ARCHIVES:
                        print("Limite de segurança de carga do s3 ativado")
                        break

                counter = counter + 1

                file_name = f"{name}/{name}_{self.time_now}.json"
                file_path = f"{path}{file_name}"
                route_path = f"{route}{file_name}"

                if not os.path.exists(file_path):
                    print(f"Pulando envio ao S3 (arquivo não gerado): {file_name}")
                    continue

                try:
                    self.s3_client.upload_file(
                        Filename=file_path,
                        Bucket=self.S3_BUCKET,
                        Key=route_path
                    )
                    print(f"Enviado {file_name}. Arquivo {counter} | Limite {self.MAX_ARCHIVES}")

                except ClientError as erro:
                    print(f"Erro ao enviar {file_name}: {erro}")

    def exec_all_brapi(self):
        self.write_json()
        self.save_files()

# %%

pipeline = Brapi_S3_Pipeline_Cdc(
    S3_BUCKET=S3_BUCKET,
    S3_REGION=S3_REGION,
    all_url=all_url,
    all_lists=all_lists,
    all_path_storage=all_path_storage,
    all_s3_route=all_s3_route
    ).exec_all_brapi()
