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
BRAPI_TOKEN = os.getenv("BRAPI_TOKEN")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")
s3_route_alpha = "painel_macro/cdc/alpha/yuan/"
path_storage_alpha = "./storage/alpha/cdc/"

colunas = [
    "date",
    "base",
    "rate"
]
