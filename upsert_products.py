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

PRODUCTS_CSV = "products.csv"

vertices = {}

with open(PRODUCTS_CSV, newline="") as f:
    reader = csv.DictReader(f)
    for row in reader:
        product_id = row["product_id"]

        vertices[product_id] = {
            "category": {
                "value": row["category"]
            },
            "price": {
                "value": float(row["price"])
            },
            "created_at": {
                "value": row["created_at"]
            }
        }

payload = {
    "vertices": {
        "Product": vertices
    }
}

response = client.upsert(payload)

print(response)
