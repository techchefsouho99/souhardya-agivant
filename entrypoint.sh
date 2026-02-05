#!/bin/bash
set -e  # 🚨 exit immediately if any command fails

echo "Starting TigerGraph bootstrap..."

echo "1️⃣ Creating vertices..."
python schema/create_vertices.py

echo "2️⃣ Creating Transaction edge..."
python schema/create_transaction_edge.py

echo "3️⃣ Adding vertices to graph..."
python schema/add_vertices_to_graph.py

echo "4️⃣ Adding Transaction edge to graph..."
python schema/add_transaction_edge_to_graph.py

echo "5️⃣ Upserting users..."
python upsert_users.py

echo "6️⃣ Upserting products..."
python upsert_products.py

echo "7️⃣ Upserting transactions..."
python upsert_transactions.py

echo "✅ TigerGraph bootstrap completed successfully!"
