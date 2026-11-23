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

time_now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")
s3_route_frank = "painel_macro/full_load/frankfurther/yuan/"
path_storage_frank = "./storage/frankfurther/full_load/"
data_range = "from=2024-01-01&to=2026-10-29"

colunas = [
    "date",
    "base",
    "rate"
]
class Etl_Frankfurther_Cdc:
    def __init__(self, 
                 S3_BUCKET: str,
                 S3_REGION: str, 
                 s3_route_frank: str, 
                 path_storage_frank: str, 
                 data_range: str
                 ):
        self.S3_BUCKET = S3_BUCKET
        self.s3_route_frank = s3_route_frank
        self.path_storage_frank = path_storage_frank
        self.time_now = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        self.s3_client = boto3.client("s3", region_name=S3_REGION)
        self.data_range = data_range

    def etl_parquet(self):
        url = f"https://api.frankfurter.dev/v2/rates?base=CNY&quotes=BRL&{self.data_range}"
        resp = requests.get(url)
        response = resp.json()
        (pd.json_normalize(response)[colunas]
         .to_parquet(f"{self.path_storage_frank}yuan_{self.time_now}.parquet", index=False))

    def sender_s3(self):
        s3_client = boto3.client("s3", region_name=S3_REGION)
        file_name = f"yuan_{self.time_now}.parquet"
        file_path = f"{self.path_storage_frank}{file_name}"
        route_path = f"{self.s3_route_frank}{file_name}"

        s3_client.upload_file(
                    Filename=file_path,
                    Bucket=self.S3_BUCKET,
                    Key=route_path
                    )

    def exec_all_frank(self):
        self.etl_parquet()
        self.sender_s3()

# %%

# pipeline = Etl_Frankfurther_Cdc(
#                 S3_BUCKET=S3_BUCKET,
#                 s3_route_frank=s3_route_frank,
#                 path_storage_frank=path_storage_frank,
#                 S3_REGION=S3_REGION,
#                 data_range=data_range
#                 ).exec_all_frank()
