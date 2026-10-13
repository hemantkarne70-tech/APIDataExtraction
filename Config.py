from datetime import datetime, timedelta

today = datetime.now()

date = (today - timedelta(days=1)).strftime("%Y-%m-%d")

URL = "XXXXXXXXXXXX"

PARAMS = {
    "ClientId": "XXXXXXXXXXXX",
    "SecretKey": "XXXXXXXXXXXX",
    "Fromdate": date, # keep empty string for dynamically updates for all data
    "Todate": date,   # keep empty string for dynamically updates for all data
}

input_path = "/opt/input/"
output_path = "/opt/output/"
error_path = "/opt/error/"

LOG_PATH = "/opt"
data_dump = "/opt/DATA_DUMP"

NEO_IP = "XXX.XXX.XXX.XXX"
NEO_PORT = "7687"


ES_URI = "XXX.XXX.XXX.XXX:9200"
ES_CONFIG = {
    "timeout": 20,
    "max_retries": 5,
    "retry_on_timeout": True,
}

pool_size = 1

col_names = {"Header": "Header", "CreatedDate": "CallCreatedDate"}
