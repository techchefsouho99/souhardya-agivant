import json
from mock_iceberg_data import USERS, PRODUCTS, TRANSACTIONS
from schema_mapping import (
    map_user_vertices,
    map_product_vertices,
    map_purchased_edges
)

def main():
    vertices = []
    edges = []

    vertices.extend(map_user_vertices(USERS))
    vertices.extend(map_product_vertices(PRODUCTS))
    edges.extend(map_purchased_edges(TRANSACTIONS))

    print("TigerGraph Vertices")
    print(json.dumps(vertices, indent=2))

    print("TigerGraph Edges")
    print(json.dumps(edges, indent=2))


if __name__ == "__main__":
    main()
