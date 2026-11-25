# %%

import os

import dotenv

dotenv.load_dotenv()

BRAPI_TOKEN = os.getenv("BRAPI_TOKEN")

s3_route_brapi = ["painel_macro/cdc/brapi/"]
path_storage_brapi = ["./storage/brapi/cdc/"]
data_range_brapi = "&interval=1d&range=5d"
# data_range_brapi = "&interval=1d&range=3mo" # Full load

extract_list = [
    "PETR4",
    "ITUB4",
    "VALE3",
    "ABEV3",
    "EMBJ3",
    "BTC"
]

name_list_brapi = [p.lower() for p in extract_list]

def extract_urls(extract_list: list[str]) -> list:

    urls = []

    for i in extract_list:
        url = f"https://brapi.dev/api/v2/stocks/historical?symbols={i}{data_range_brapi}&token={BRAPI_TOKEN}"
        urls.append(url)

    return urls

urls_brapi = extract_urls(extract_list=extract_list)