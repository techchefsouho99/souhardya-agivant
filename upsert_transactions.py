from tg_client import TigerGraphClient

client = TigerGraphClient(
    host="https://tg-441a7ba5-946d-4471-a7c0-22e5b0bc386f.tg-2635877100.i.tgcloud.io",
    token="YOUR_API_TOKEN",
    graph="CommerceGraph"
)

transactions = [
    ("t1", "u1", "p1", 19.99, "2024-01-02T10:00:00.000Z"),
    ("t2", "u1", "p2", 899.99, "2024-01-03T12:30:00.000Z"),
]

edges = {}

for txn_id, user_id, product_id, amount, ts in transactions:
    edges.setdefault("User", {}).setdefault(user_id, {}).setdefault(
        "Transaction", {}
    ).setdefault("Product", {})[product_id] = {
        "txn_id": {"value": txn_id},
        "amount": {"value": amount},
        "txn_timestamp": {"value": ts}
    }

payload = {
    "edges": edges
}

print(
    client.upsert(
        payload,
        params={"vertex_must_exist": "true"}
    )
)
