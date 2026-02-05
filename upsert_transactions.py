import os
import csv
from auth.tg_token import get_tg_token
from tg_client import TigerGraphClient

TG_HOST = os.getenv("TG_HOST")
GRAPH = "commerceGraph"

client = TigerGraphClient(
    host = TG_HOST,
    token = get_tg_token(),
    graph = GRAPH
)

TRANSACTIONS_CSV = "transactions.csv"

edges = {
    "User": {}
}

with open(TRANSACTIONS_CSV, newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        user_id = row["user_id"]
        product_id = row["product_id"]

        edges["User"] \
            .setdefault(user_id, {}) \
            .setdefault("Transaction", {}) \
            .setdefault("Product", {})[product_id] = {
                "txn_id": {
                    "value": row["txn_id"]          # discriminator
                },
                "amount": {
                    "value": float(row["amount"])  
                },
                "txn_timestamp": {
                    "value": row["txn_timestamp"]  
                }
            }

payload = {
    "edges": edges
}

response = client.upsert(
    payload,
    params={"vertex_must_exist": "true"}
)

print(response)
