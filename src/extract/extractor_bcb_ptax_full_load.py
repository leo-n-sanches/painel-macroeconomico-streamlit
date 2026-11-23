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
data_range = "@dataInicial=%2711-01-2026%27&@dataFinalCotacao=%2711-19-2026%27"

moeda = [
    "USD",
    "EUR"
]

colunas = [
    "cotacaoCompra",
    "cotacaoVenda",
    "dataHoraCotacao",
    "tipoBoletim"
]

# %%

moeda = "USD"

# Histórico

# Dólar = https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda=%27USD%27&@dataInicial=%2711-01-2026%27&@dataFinalCotacao=%2711-19-2026%27&$format=json

# Euro = https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda=%27EUR%27&@dataInicial=%2711-01-2026%27&@dataFinalCotacao=%2711-19-2026%27&$format=json

url = f"https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaPeriodo(moeda=@moeda,dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)?@moeda=%27{moeda}%27&{data_range}&$format=json"


resp = requests.get(url)
response = resp.json()
df = pd.json_normalize(response, record_path=['value'])[colunas]

print(df)
# %%