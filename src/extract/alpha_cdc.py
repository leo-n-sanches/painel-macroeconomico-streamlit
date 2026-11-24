# %%

import os

import dotenv

dotenv.load_dotenv()

ALPHA_TOKEN = os.getenv("ALPHA_TOKEN")
s3_route_alpha = ["painel_macro/cdc/alpha/"]
path_storage_alpha = ["./storage/alpha/cdc/"]

name_list_alpha = [
    "aapl",
    "amzn",
    "googl",
    "msft",
    "nvda"
]

def extract_urls(name_list_alpha: list[str]) -> list:

    urls = []

    for i in name_list_alpha:
        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={i}&apikey={ALPHA_TOKEN}"
        urls.append(url)

    return urls

urls_alpha = extract_urls(name_list_alpha=name_list_alpha)
