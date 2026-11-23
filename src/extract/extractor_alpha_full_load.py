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
s3_route_alpha = "painel_macro/full_load/alpha/"
path_storage_alpha = "./storage/alpha/full_load/"
data_range = "from=2024-01-01&to=2026-10-29"

colunas = [
    "date",
    "base",
    "rate"
]
