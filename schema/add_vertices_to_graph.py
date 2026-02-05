import os , requests , json
from auth.tg_token import get_tg_token

TG_HOST = os.getenv("TG_HOST")
TG_TOKEN = get_tg_token()
GRAPH = "commerceGraph"

url = f"{TG_HOST}/gsql/v1/schema/vertices"
params = {"graph": GRAPH}

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TG_TOKEN}"
}

payload = {
    "addVertices": [
        "User",
        "Product"
    ]
}

response = requests.post(
    url,
    headers=headers,
    params=params,
    data=json.dumps(payload)
)

print("Status:", response.status_code)
print(json.dumps(response.json(), indent=2))
