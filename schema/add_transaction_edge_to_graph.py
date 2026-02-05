import requests
import json
import os
from auth.tg_token import get_tg_token

TG_HOST = os.getenv("TG_HOST")
GRAPH = "commerceGraph"

TG_TOKEN = get_tg_token()

URL = f"{TG_HOST}/gsql/v1/schema/edges"
PARAMS = {"graph": GRAPH}

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TG_TOKEN}"
}

payload = {
    "addEdges": [
        "Transaction"
    ]
}

response = requests.post(
    URL,
    headers=HEADERS,
    params=PARAMS,
    data=json.dumps(payload)
)

print("Status Code:", response.status_code)
print(json.dumps(response.json(), indent=2))
