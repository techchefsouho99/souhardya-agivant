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
## How the Pipeline Works (Walkthrough)

### Step 1: Generate Token

- auth/tg_token.py requests a TigerGraph token
- Token is cached for reuse

### Step 2: Create Schema

- Vertices (User, Product) created via REST GSQL
- Edge (Transaction) created with discriminator
- Schema additions are idempotent

### Step 3: Upsert Vertices

- users.csv → User vertices
- products.csv → Product vertices
- Uses REST++ /restpp/graph/{graph} endpoint

### Step 4: Upsert Edges

- transactions.csv → Transaction edges
- Ensures both vertices exist (vertex_must_exist=true)
- Discriminator guarantees edge uniqueness

### Step 5: Validation

- Graph Studio Explore confirms:
- 1. User → Product connections
- 2. Multiple transactions per pair supported

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

**Chosen approach: Batch ingestion**

Batch ingestion is preferred because:
- Iceberg is snapshot-oriented
- TigerGraph supports high-throughput batch-oriented ingestion via REST++ upserts and native loaders
- Batch jobs are simpler to operate, debug, and rerun

Streaming ingestion is acknowledged as a future extension for low-latency use cases but introduces additional operational complexity.

---

### Push vs Pull

**Chosen approach: Push-based ingestion**

In this design:
- Spark reads from Iceberg and pushes data into TigerGraph
- Governance is enforced centrally via Unity Catalog
- Transformation logic remains outside TigerGraph

Pull-based ingestion would require custom connectors and duplicate governance logic, increasing system complexity.

---

## Prototype Execution Modes

The prototype supports two execution modes:

### Databricks Mode (Full Integration)
- Spark reads Apache Iceberg tables using Unity Catalog identifiers
- Schema discovery and access control are enforced by Unity Catalog
- Data is transformed using Spark DataFrames
- Vertex and edge data is upserted into TigerGraph using REST++ APIs

This mode is intended to run inside a Databricks workspace with Unity Catalog enabled.

### Local Mode (Dry Run)
- Unity Catalog and Iceberg tables are not available locally
- The pipeline falls back to minimal mock data
- Real TigerGraph REST++ payloads are generated and printed
- No TigerGraph instance is required

This mode validates transformation logic and TigerGraph API correctness without requiring full infrastructure.

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
