import requests

class TigerGraphClient:
    def __init__(self, host, token, graph):
        self.base_url = f"{host}/restpp/graph/{graph}"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "gsql-atomic-level": "atomic"   # all-or-nothing
        }

    def upsert(self, payload, params=None):
        r = requests.post(
            self.base_url,
            json=payload,
            headers=self.headers,
            params=params or {}
        )
        r.raise_for_status()
        return r.json()
