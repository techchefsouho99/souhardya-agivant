# Iceberg → TigerGraph Integration Prototype

## Overview

This repository contains a push-based data integration prototype that demonstrates how data stored in Apache Iceberg (on S3) can be transformed and ingested into TigerGraph Cloud (Savanna) using:

- **Spark** for data processing
- **REST++ APIs** for graph ingestion
- **Idempotent upserts** for reliability
- **Docker** for repeatable execution

The prototype focuses on **design clarity and correctness**, showing how Iceberg-style relational data can be modeled, transformed, and reliably ingested into a graph system.

---

## Problem Statement

The goal of this project is to design and implement a pipeline that:

1. Reads relational / tabular data (Iceberg-style schemas)
2. Maps tabular entities into a **property graph**
3. Creates TigerGraph schema **programmatically**
4. Loads vertices and edges using **REST++ upserts**
5. Supports **repeatable, idempotent, batch ingestion**
6. Can be executed locally or via Docker

This repository demonstrates **how Iceberg-style datasets can be modeled and ingested into TigerGraph reliably**, without relying on manual GraphStudio steps.

---

## High-Level Architecture
```text
Apache Iceberg (S3)
  (Snapshot-based tables)
        ↓
Spark / Python
  (DataFrames or CSV export)
        ↓
Relational → Graph Mapping
  (Entities → Vertices, FKs → Edges)
        ↓
TigerGraph REST++ APIs
  (Idempotent upserts)
        ↓
TigerGraph Cloud (Savanna)
```
---

## Graph Modeling Approach

### Vertex Types
```
CREATE VERTEX User (
  PRIMARY_ID user_id STRING,
  username STRING,
  email STRING,
  created_at DATETIME
)

CREATE VERTEX Product (
  PRIMARY_ID product_id STRING,
  category STRING,
  price FLOAT,
  created_at DATETIME
)
```

### Edge Type
```
CREATE DIRECTED EDGE Transaction (
  FROM User,
  TO Product,
  DISCRIMINATOR (txn_id STRING),
  amount FLOAT,
  txn_timestamp DATETIME
)
```

### Why a Discriminator?
Using ```txn_id``` as a DISCRIMINATOR allows:

- Multiple transactions between the same User and Product
- Unique identification of each transaction
- Safe re-upserts without overwriting previous edges

---

## Authentication Design

### Token Generation
TigerGraph tokens are generated once per process using:

```
POST /gsql/v1/tokens
```
The token is:
- Cached in memory
- Reused across all schema and upsert calls
-  Never hardcoded in scripts
Environment variables:
```
TG_HOST=https://<tgcloud-host>
TG_SECRET=<gsql-secret>
```

---
## TigerGraph Ingestion Pipeline (Code Walkthrough)
This section explains how the **TigerGraph pipeline works end-to-end in code**.

The pipeline is intentionally split into **ordered**, **explicit phases** to avoid hidden behavior and to make failures easy to diagnose.

### Phase 1: Schema Creation (Vertices & Edges)
Schema creation is handled programmatically using the GSQL Schema REST API.

- Vertex schemas (```User```, ```Product```) are created first
- Edge schema (```Transaction```) is created with a discriminator
- Schema creation is idempotent — re-running the pipeline is safe

### Phase 2: Graph Wiring (Attaching Schema to the Graph)

In TigerGraph, **schema definition and graph membership are separate concerns**.

After defining vertex and edge schemas globally, they must be explicitly attached to the target graph (e.g. ```commerceGraph```).

Conceptually:
```
ALTER GRAPH commerceGraph ADD VERTEX User, Product;
ALTER GRAPH commerceGraph ADD EDGE Transaction;
```
This step is critical:
- Without it, REST++ upserts may succeed
- But vertices and edges will not appear in Graph Explorer or queries

The pipeline performs this wiring via REST APIs to ensure the graph is fully usable without manual intervention.

### Phase 3: Vertex Upserts (Users & Products)

Vertex ingestion is driven from CSV files:
- ```users.csv``` → User vertices
- ```products.csv``` → Product vertices
Each row is converted into a REST++ payload of the form:
```
{
  "vertices": {
    "User": {
      "u1": {
        "username": { "value": "alice" },
        "email": { "value": "alice@example.com" },
        "created_at": { "value": "2026-02-02T23:27:24.288Z" }
      }
    }
  }
}
```
REST++ **upsert semantics** ensure:

- Missing vertices are created
- Existing vertices are updated
- Re-running the pipeline does not create duplicates

### Phase 4: Edge Upserts (Transactions)

Transactions are ingested as **discriminated edges**.
Each row in ```transactions.csv``` becomes a unique edge identified by:
```
(User → Product, txn_id)
```
Conceptual payload:
```
{
  "edges": {
    "User": {
      "u1": {
        "Transaction": {
          "Product": {
            "p1": {
              "txn_id": { "value": "t1" },
              "amount": { "value": 19.99 },
              "txn_timestamp": { "value": "2024-01-02T10:00:00.000Z" }
            }
          }
        }
      }
    }
  }
}
```
Key guarantees:
- Multiple transactions between the same User and Product are preserved
- No accidental overwrites occur
- Idempotent retries are safe

### Phase 5: Validation

After ingestion:
- GraphStudio Explore shows User → Product connectivity
- Multiple Transaction edges per pair are visible
- Graph queries return correct results

## TigerGraph Schema Visualization
The following diagram shows the actual graph schema and data loaded into TigerGraph Cloud, including `User` and `Product` vertices connected by `Transaction` edges.

![TigerGraph Graph Schema](docs/tigergraph-schema.png)

## Execution Options
### Option 1: Local (Python)
```
export TG_HOST=...
export TG_SECRET=...

python upsert_users.py
python upsert_products.py
python upsert_transactions.py
```
### Option 2: Docker (Recommended)
#### Build
```
docker build -t agivant-tg-bootstrap .
```
#### Run
```
docker run --rm \
  -e TG_HOST="https://<tgcloud-host>" \
  -e TG_SECRET="<gsql-secret>" \
  agivant-tg-bootstrap
```
Docker guarantees:

- Correct execution order
- Clean environment
- One-shot bootstrap behavior


## Prototype Scope

This prototype is intentionally lightweight and demonstrates:

- Spark-based ingestion logic for Apache Iceberg tables
- Unity Catalog–based schema discovery and access control
- Explicit relational-to-graph schema mapping
- Generation of TigerGraph REST++ upsert payloads
- Graceful fallback when full infrastructure is unavailable

It does **not** require:
- A locally running Databricks workspace
- A locally running TigerGraph instance

---

## Tradeoff Summary

### Batch vs Streaming

#### Chosen approach: Batch ingestion

Batch ingestion is preferred because:
- Iceberg is snapshot-oriented
- TigerGraph supports high-throughput batch-oriented ingestion via REST++ upserts and native loaders
- Batch jobs are simpler to operate, debug, and rerun

Streaming ingestion is acknowledged as a future extension for low-latency use cases but introduces additional operational complexity.

### Push vs Pull

#### Chosen approach: Push-based ingestion**

In this design:
- Spark reads from Iceberg and pushes data into TigerGraph
- Governance is enforced centrally via Unity Catalog
- Transformation logic remains outside TigerGraph

Pull-based ingestion would require custom connectors and duplicate governance logic, increasing system complexity.

---

## Fault Tolerance and Reliability

The pipeline is designed to be fault tolerant by construction:

- **Iceberg snapshots** ensure consistent, repeatable reads
- **Spark transformations** are deterministic and retryable
- **Unity Catalog** enforces schema and permission validation at read time
- **TigerGraph REST++ upserts** are idempotent, allowing safe retries
- Partial failures can be recovered by replaying the same snapshot

This design avoids duplicate graph entities and supports safe reprocessing.

---

## How to Run the Prototype

### Notes on Execution

- Spark and Unity Catalog integration is intended to run in Databricks
- Local execution demonstrates fallback behavior and REST++ payload generation
- Dry-run mode avoids requiring a running TigerGraph instance
