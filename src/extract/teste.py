# %%

import os

import dotenv
import pandas as pd
import pyarrow
import requests
import sqlalchemy

dotenv.load_dotenv()

path_storage = "./storage/teste.parquet"

df2 = pd.read_parquet(path=path_storage)

df2