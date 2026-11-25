# %%

from datetime import datetime, timezone, timedelta

time_delay_7days = (datetime.now(timezone.utc) - timedelta(days=6)).strftime("%Y-%m-%d")
time_now = datetime.now(timezone.utc).strftime("%Y-%m-%d")

s3_route_frank = ["painel_macro/cdc/frankfurther/"]
path_storage_frank = ["./storage/frankfurther/cdc/"]
name_list_frank = ["yuan"]
data_range_frank = f"from={time_delay_7days}&to={time_now}" #YYYY-MM-DD
# data_range_frank = f"from=2019-01-01&to={time_now}" # Full load just change dates on format YYYY-MM-DD

urls_frank = [f"https://api.frankfurter.dev/v2/rates?base=CNY&quotes=BRL&{data_range_frank}"]