# %%

s3_route_frank = ["painel_macro/full_load/frankfurther/"]
path_storage_frank = ["./storage/frankfurther/full_load/"]
name_list_frank = ["yuan"]
data_range_frank = "from=2024-01-01&to=2026-10-29"
urls_frank = [f"https://api.frankfurter.dev/v2/rates?base=CNY&quotes=BRL&{data_range_frank}"]