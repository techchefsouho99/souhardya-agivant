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

USERS_CSV = "users.csv"

vertices = {}

with open(USERS_CSV, newline="") as f:
    reader = csv.DictReader(f)

    for row in reader:
        user_id = row["user_id"]

        vertices[user_id] = {
            "username": {
                "value": row["username"]
            },
            "email": {
                "value": row["email"]
            },
            "created_at": {
                "value": row["created_at"]
            }
        }

payload = {
    "vertices": {
        "User": vertices
    }
}

response = client.upsert(payload)
print(response)
