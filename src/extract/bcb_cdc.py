# %%

s3_route_bcb = ["painel_macro/cdc/bcb/"]
path_storage_bcb = ["./storage/bcb/cdc/"]

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
        url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{i}/dados/ultimos/1?formato=json"
        urls.append(url)

    return urls

urls_bcb = extract_urls(codigo_sgs=codigo_sgs)