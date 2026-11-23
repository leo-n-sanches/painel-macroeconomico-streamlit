# %%

import os

import dotenv
import pandas as pd
import requests

dotenv.load_dotenv()
BRAPI_TOKEN = os.getenv("BRAPI_TOKEN")

# %%

path_storage1 = "./storage/bcb/full_load/dolar_20261123T200328Z.parquet"
# path_storage2 = "./storage/BTC_full_load.parquet"

df1 = pd.read_parquet(path=path_storage1)
# df2 = pd.read_parquet(path=path_storage2)

print(df1)
# print(df2)

# %%

df1 = df1.to_csv("daily.csv", sep=";")
# df2 = df2.to_csv("full_load.csv", sep=";")

# %%

colunas = [
    "symbol",
    "volume",
    "close",
    "low",
    "high",
    "open",
    "date"
]

colunas_novas = {
    "results.symbol": "symbol",
    "volume": "volume",
    "close": "close",
    "low": "low",
    "high": "high",
    "open": "open",
    "date": "date"
}

url = f"https://brapi.dev/api/v2/stocks/historical?symbols=BTC&interval=1d&range=3mo&token={BRAPI_TOKEN}"

resp = requests.get(url)
response = resp.json()
df_temp = pd.json_normalize(response, 
                            record_path=['results', 'data', 'historicalDataPrice'],
                            meta=[['results', 'symbol']]
                            )

df = df_temp.rename(columns=colunas_novas)[colunas]
print(df)
# %%
