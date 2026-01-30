def map_user_vertices(users):
    return [
        {
            "vertex_type": "User",
            "primary_id": u["user_id"],
            "attributes": {
                "name": u["name"],
                "email": u["email"],
                "created_at": u["created_at"]
            }
        }
        for u in users
    ]


def map_product_vertices(products):
    return [
        {
            "vertex_type": "Product",
            "primary_id": p["product_id"],
            "attributes": {
                "category": p["category"],
                "price": p["price"],
                "created_at": p["created_at"]
            }
        }
        for p in products
    ]


def map_purchased_edges(transactions):
    return [
        {
            "edge_type": "PURCHASED",
            "from_type": "User",
            "from_id": t["user_id"],
            "to_type": "Product",
            "to_id": t["product_id"],
            "attributes": {
                "txn_id": t["txn_id"],
                "amount": t["amount"],
                "timestamp": t["timestamp"]
            }
        }
        for t in transactions
    ]
