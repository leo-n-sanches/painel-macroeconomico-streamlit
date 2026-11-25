# %%
from datetime import datetime, timezone, timedelta

s3_route_bcb = ["painel_macro/cdc/bcb/"]
path_storage_bcb = ["./storage/bcb/cdc/"]

time_delay_10days = (datetime.now(timezone.utc) - timedelta(days=9)).strftime("%d/%m/%Y")
time_delay_45days = (datetime.now(timezone.utc) - timedelta(days=45)).strftime("%d/%m/%Y")
time_now = datetime.now(timezone.utc).strftime("%d/%m/%Y")

# data_inicio = "01/01/2019" # Full load on format DD/MM/YYYY
# data_range = f"dataInicial={data_inicio}&dataFinal={time_now}" # Full load on format DD/MM/YYYY

urls_bcb = [
            f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json&dataInicial={time_delay_10days}&dataFinal={time_now}",
            f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json&dataInicial={time_delay_45days}&dataFinal={time_now}"
            ]

codigo_sgs = [
    "432", # selic
    "433" # IPCA
    ]

name_list_bcb = [
    "selic",
    "ipca"
    ]

print(urls_bcb)