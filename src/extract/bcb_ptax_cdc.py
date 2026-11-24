# %%

from datetime import datetime, timezone

s3_route_ptax = ["painel_macro/cdc/bcb/"]
path_storage_ptax = ["./storage/bcb/cdc/"]

moeda = [
    "USD",
    "EUR"
]

name_list_ptax = [
    "dolar",
    "euro"
]

data_ptax = datetime.now(timezone.utc).strftime("%m-%d-%Y")

def extract_urls(moeda: list[str]) -> list:

    urls = []

    for i in moeda:
        url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=%27{i}%27&@dataCotacao=%27{data_ptax}%27&$format=json"
        urls.append(url)

    return urls

urls_ptax = extract_urls(moeda=moeda)