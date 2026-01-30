# spark_to_rest.py

def users_to_vertex_payload(df):
    return [
        {
            "id": row["user_id"],
            "attributes": {
                "username": row["username"],
                "email": row["email"],
                "created_at": str(row["created_at"])
            }
        }
        for row in df.collect()
    ]


def products_to_vertex_payload(df):
    return [
        {
            "id": row["product_id"],
            "attributes": {
                "category": row["category"],
                "price": row["price"],
                "created_at": str(row["created_at"])
            }
        }
        for row in df.collect()
    ]


def transactions_to_edge_payload(df):
    return [
        {
            "from_id": row["user_id"],
            "to_id": row["product_id"],
            "attributes": {
                "txn_id": row["txn_id"],
                "amount": row["amount"],
                "timestamp": str(row["timestamp"])
            }
        }
        for row in df.collect()
    ]
