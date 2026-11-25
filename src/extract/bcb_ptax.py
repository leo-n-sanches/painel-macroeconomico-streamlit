# %%
from datetime import datetime, timezone, timedelta

s3_route_ptax = ["painel_macro/cdc/bcb/"]
path_storage_ptax = ["./storage/bcb/cdc/"]

time_delay_7days = (datetime.now(timezone.utc) - timedelta(days=6)).strftime("%m-%d-%Y")
time_now = datetime.now(timezone.utc).strftime("%m-%d-%Y")

data_inicio = time_delay_7days
data_final = time_now
data_range = f"@dataInicial=%27{data_inicio}%27&@dataFinalCotacao=%27{data_final}%27" # MM-DD-YYYY
# data_range = f"@dataInicial=%2701-01-2019%27&@dataFinalCotacao=%27{data_final}%27" # Full load on format MM-DD-YYYY

moeda = [
    "USD",
    "EUR"
]

name_list_ptax = [
    "dolar",
    "euro"
]

def extract_urls(moeda: list[str]) -> list:

    urls = []

    for i in moeda:
        url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda=%27{i}%27&{data_range}&$format=json"
        urls.append(url)

    return urls

urls_ptax = extract_urls(moeda=moeda)