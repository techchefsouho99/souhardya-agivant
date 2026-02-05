from tg_client import TigerGraphClient

client = TigerGraphClient(
    host="https://tg-441a7ba5-946d-4471-a7c0-22e5b0bc386f.tg-2635877100.i.tgcloud.io",
    token="YOUR_API_TOKEN",
    graph="CommerceGraph"
)

products = [
    ("p1", "Books", 19.99, "2026-02-02T23:26:10.659Z"),
    ("p2", "Electronics", 899.99, "2026-02-02T23:26:10.659Z"),
]

payload = {
    "vertices": {
        "Product": {
            pid: {
                "category": {"value": category},
                "price": {"value": price},
                "created_at": {"value": created_at}
            }
            for pid, category, price, created_at in products
        }
    }
}

print(client.upsert(payload))
