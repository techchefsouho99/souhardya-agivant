from tg_client import TigerGraphClient

client = TigerGraphClient(
    host="https://tg-441a7ba5-946d-4471-a7c0-22e5b0bc386f.tg-2635877100.i.tgcloud.io",
    token="MY_API_TOKEN",
    graph="CommerceGraph"
)
 
users = [
    ("u1", "alice", "alice@example.com", "2026-02-02T23:27:24.288Z"),
    ("u2", "bob", "bob@example.com", "2026-02-02T23:27:24.288Z"),
]

payload = {
    "vertices": {
        "User": {
            uid: {
                "username": {"value": username},
                "email": {"value": email},
                "created_at": {"value": created_at}
            }
            for uid, username, email, created_at in users
        }
    }
}

print(client.upsert(payload))
