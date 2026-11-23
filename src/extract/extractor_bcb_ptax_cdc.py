# %%

import os
from datetime import datetime, timezone

import boto3
import dotenv
import pandas as pd
import requests
from botocore.exceptions import ClientError

dotenv.load_dotenv()

# %%

S3_BUCKET = os.getenv("S3_BUCKET")
S3_REGION = os.getenv("S3_REGION")

s3_route_bcb = "painel_macro/cdc/bcb/"
path_storage_bcb = "./storage/bcb/cdc/"

moeda = [
    "USD",
    "EUR"
]

moeda_save = [
    "dolar",
    "euro"
]

# %%

# Diário

# Dólar = https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=%27USD%27&@dataCotacao=%2711-19-2026%27&$format=json
# Euro = https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=%27EUR%27&@dataCotacao=%2711-19-2026%27&$format=json

# %%

# OBSERVAÇÃO, o URL PTAX RETORNA VAZIO NOS FINAIS DE SEMANA

# data_ptax = datetime.now(timezone.utc).strftime("") # tem que ter esse formato 11-22-2026

data_ptax = "11-16-2026"
moeda = "USD"

url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)?@moeda=%27{moeda}%27&@dataCotacao=%27{data_ptax}%27&$format=json"
resp = requests.get(url)
response = resp.json()
df = pd.json_normalize(response, record_path=['value'])

# DIVIDIR EM 2 - PTAX e TAXAS


print(df)
# %%

df.to_parquet("./storage/bcb/cdc/dolar/dolar_teste.parquet", index=False)