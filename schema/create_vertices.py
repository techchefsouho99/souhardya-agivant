import os
import requests
import json
from auth.tg_token import get_tg_token

TG_HOST = os.getenv("TG_HOST")
TG_TOKEN = get_tg_token()


URL = f"{TG_HOST}/gsql/v1/schema/vertices"

HEADERS = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {TG_TOKEN}"
}

payload = {
    "createVertices": [
        {
            "Name": "User",
            "PrimaryId": {
                "AttributeName": "user_id",
                "AttributeType": {"Name": "STRING"}
            },
            "Attributes": [
                {
                    "AttributeName": "username",
                    "AttributeType": {"Name": "STRING"}
                },
                {
                    "AttributeName": "email",
                    "AttributeType": {"Name": "STRING"}
                },
                {
                    "AttributeName": "created_at",
                    "AttributeType": {"Name": "DATETIME"}
                }
            ],
            "Config": {
                "STATS": "OUTDEGREE_BY_EDGETYPE"
            }
        },
        {
            "Name": "Product",
            "PrimaryId": {
                "AttributeName": "product_id",
                "AttributeType": {"Name": "STRING"}
            },
            "Attributes": [
                {
                    "AttributeName": "category",
                    "AttributeType": {"Name": "STRING"}
                },
                {
                    "AttributeName": "price",
                    "AttributeType": {"Name": "FLOAT"}
                },
                {
                    "AttributeName": "created_at",
                    "AttributeType": {"Name": "DATETIME"}
                }
            ],
            "Config": {
                "STATS": "OUTDEGREE_BY_EDGETYPE"
            }
        }
    ]
}

response = requests.post(
    URL,
    headers=HEADERS,
    data=json.dumps(payload)
)

print("Status Code:", response.status_code)
print(json.dumps(response.json(), indent=2))
