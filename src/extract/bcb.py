# %%
from datetime import datetime, timezone, timedelta

s3_route_bcb = ["painel_macro/cdc/bcb/"]
path_storage_bcb = ["./storage/bcb/cdc/"]

time_delay_7days = (datetime.now(timezone.utc) - timedelta(days=6)).strftime("%d/%m/%Y")
time_now = datetime.now(timezone.utc).strftime("%d/%m/%Y")

data_inicio = time_delay_7days
data_final = time_now
data_range = f"dataInicial={data_inicio}&dataFinal={data_final}" # DD/MM/YYYY
# data_range = f"dataInicial=01/01/2019&dataFinal={data_final}" # Full load on format DD/MM/YYYY

codigo_sgs = [
    "432", # selic
    "433" # IPCA
    ]

name_list_bcb = [
    "selic",
    "ipca"
    ]

def extract_urls(codigo_sgs: list[str]) -> list:

    urls = []

    for i in codigo_sgs:
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{i}/dados?formato=json&{data_range}"
        urls.append(url)

    return urls

urls_bcb = extract_urls(codigo_sgs=codigo_sgs)