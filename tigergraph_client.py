# tigergraph_client.py

import requests
import json

class TigerGraphClient:
    def __init__(self, host, graph, token, dry_run=False):
        self.base_url = f"{host}/restpp/graph/{graph}"
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        self.dry_run = dry_run

    def upsert_vertices(self, vertex_type, records):
        payload = {
            "vertices": {
                vertex_type: {
                    r["id"]: {"attributes": r["attributes"]}
                    for r in records
                }
            }
        }

        if self.dry_run:
            print(f"[DRY RUN] Vertex upsert ({vertex_type}):")
            print(json.dumps(payload, indent=2))
            return

        try:
            resp = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=5
            )
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("TigerGraph connection failed.")
            print("Falling back to dry-run mode.")
            print(json.dumps(payload, indent=2))

    def upsert_edges(self, edge_type, records):
        payload = {
            "edges": {
                edge_type: records
            }
        }

        if self.dry_run:
            print(f"[DRY RUN] Edge upsert ({edge_type}):")
            print(json.dumps(payload, indent=2))
            return

        try:
            resp = requests.post(
                self.base_url,
                headers=self.headers,
                data=json.dumps(payload),
                timeout=5
            )
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            print("TigerGraph connection failed.")
            print("Falling back to dry-run mode.")
            print(json.dumps(payload, indent=2))

