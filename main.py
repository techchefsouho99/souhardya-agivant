# import json
# from mock_iceberg_data import USERS, PRODUCTS, TRANSACTIONS
# from schema_mapping import (
#     map_user_vertices,
#     map_product_vertices,
#     map_purchased_edges
# )

# def main():
#     vertices = []
#     edges = []

#     vertices.extend(map_user_vertices(USERS))
#     vertices.extend(map_product_vertices(PRODUCTS))
#     edges.extend(map_purchased_edges(TRANSACTIONS))

#     print("TigerGraph Vertices")
#     print(json.dumps(vertices, indent=2))

#     print("TigerGraph Edges")
#     print(json.dumps(edges, indent=2))


# if __name__ == "__main__":
#     main()

# main.py

from tigergraph_client import TigerGraphClient
from spark_to_rest import (
    users_to_vertex_payload,
    products_to_vertex_payload,
    transactions_to_edge_payload
)

# Attempt to load Spark + Unity Catalog (Databricks)

try:
    from spark_read_iceberg import users_df, products_df, transactions_df
    from transform_to_graph import (
        map_user_vertices,
        map_product_vertices,
        map_purchased_edges
    )

    spark_mode = "databricks"
    print("Running in Databricks mode (Unity Catalog enabled)")

except Exception as e:
    spark_mode = "local"
    print("Unity Catalog not available locally.")
    print("Falling back to local mock data.")
    print(f"Reason: {e}")

# TigerGraph Configuration

TG_HOST = "http://localhost:9000"
TG_GRAPH = "CommerceGraph"
TG_TOKEN = "<YOUR_TIGERGRAPH_TOKEN>"

tg = TigerGraphClient(
    host=TG_HOST,
    graph=TG_GRAPH,
    token=TG_TOKEN,
    dry_run=True
)

# Databricks Execution Path

if spark_mode == "databricks":
    # Transform Spark DataFrames
    user_vertices_df = map_user_vertices(users_df)
    product_vertices_df = map_product_vertices(products_df)
    purchase_edges_df = map_purchased_edges(transactions_df)

    # Convert to REST++ payloads
    user_vertices = users_to_vertex_payload(user_vertices_df)
    product_vertices = products_to_vertex_payload(product_vertices_df)
    purchase_edges = transactions_to_edge_payload(purchase_edges_df)

# Local Mock Execution Path

else:
    # Minimal mock data for local execution
    user_vertices = [
        {
            "id": "u1",
            "attributes": {
                "username": "alice",
                "email": "alice@example.com",
                "created_at": "2024-01-01T00:00:00Z"
            }
        }
    ]

    product_vertices = [
        {
            "id": "p1",
            "attributes": {
                "category": "books",
                "price": 19.99,
                "created_at": "2024-01-01T00:00:00Z"
            }
        }
    ]

    purchase_edges = [
        {
            "from_id": "u1",
            "to_id": "p1",
            "attributes": {
                "txn_id": "t1",
                "amount": 19.99,
                "timestamp": "2024-01-02T10:00:00Z"
            }
        }
    ]

# Ingest into TigerGraph (REST++ Upserts)

print("Upserting vertices and edges into TigerGraph...")

tg.upsert_vertices("User", user_vertices)
tg.upsert_vertices("Product", product_vertices)
tg.upsert_edges("PURCHASED", purchase_edges)

print("Ingestion completed successfully.")
