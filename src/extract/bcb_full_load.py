# %%

s3_route_bcb = ["painel_macro/full_load/bcb/"]
path_storage_bcb = ["./storage/bcb/full_load/"]

data_inicio = "01-01-2026"
data_final = "11-23-2026"
data_range = f"dataInicial={data_inicio}&dataFinal={data_final}"

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