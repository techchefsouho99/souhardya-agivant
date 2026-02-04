import requests

HOST = "https://tg-441a7ba5-946d-4471-a7c0-22e5b0bc386f.tg-2635877100.i.tgcloud.io"
TOKEN = "<API_TOKEN>"

url = f"{HOST}/restpp/gsql/v1/loading-jobs/run"

payload = {
    "graph": "CommerceGraph",
    "job": "load_commerce_data",
    "files": {
        "users_file": "s3://bucket/users.csv",
        "products_file": "s3://bucket/products.csv",
        "transactions_file": "s3://bucket/transactions.csv"
    }
}

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Content-Type": "application/json"
}

r = requests.post(url, json=payload, headers=headers)
print(r.json())
