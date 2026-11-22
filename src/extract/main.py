# %%

import os

import dotenv
from extractor_brapi_cdc import (
            Brapi_S3_Pipeline_Cdc,
            extract_list,
            extract_list_small,
            path_storage_brapi,
            s3_route_brapi,
)
from extractor_frank_cdc import Etl_Frankfurther_Cdc, path_storage_frank, s3_route_frank

dotenv.load_dotenv()

# %%

BRAPI_TOKEN = os.getenv("BRAPI_TOKEN")
S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")

# %%

Brapi_S3_Pipeline_Cdc(
            S3_BUCKET=S3_BUCKET,
            s3_route_brapi=s3_route_brapi,
            path_storage_brapi=path_storage_brapi,
            S3_REGION=S3_REGION,
            BRAPI_TOKEN=BRAPI_TOKEN
    ).exec_all_brapi(
            extract_list=extract_list, 
            extract_list_small=extract_list_small
            )

# %%

Etl_Frankfurther_Cdc(
    S3_BUCKET=S3_BUCKET,
    s3_route_frank=s3_route_frank,
    path_storage_frank=path_storage_frank,
    S3_REGION=S3_REGION,
    BRAPI_TOKEN=BRAPI_TOKEN
    ).exec_all_frank()

# %%