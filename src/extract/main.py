# %%

import os
import dotenv
from extract_brapi_daily import Brapi_S3_Pipeline_cdc, extract_list, extract_list_small, path_storage, s3_route

dotenv.load_dotenv()

# %%

BRAPI_TOKEN = os.getenv("BRAPI_TOKEN")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")

Brapi_S3_Pipeline_cdc(
            S3_BUCKET=S3_BUCKET,
            s3_route=s3_route,
            path_storage=path_storage,
            S3_REGION=S3_REGION,
            BRAPI_TOKEN=BRAPI_TOKEN
    ).exec_all(
            extract_list=extract_list, 
            extract_list_small=extract_list_small
            )

# %%
