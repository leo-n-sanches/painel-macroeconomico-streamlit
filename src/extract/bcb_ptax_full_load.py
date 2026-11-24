# %%

s3_route_ptax = ["painel_macro/full_load/bcb/"]
path_storage_ptax = ["./storage/bcb/full_load/"]

data_inicio = "01-01-2026"
data_final = "11-23-2026"
data_range = f"@dataInicial=%27{data_inicio}%27&@dataFinalCotacao=%27{data_final}%27"

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