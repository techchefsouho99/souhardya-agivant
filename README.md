# Iceberg → TigerGraph Integration Prototype

## Overview

This repository contains a push-based data integration prototype that demonstrates how data stored in Apache Iceberg (on S3) can be transformed and ingested into TigerGraph Cloud (Savanna) using:

- Spark for data processing
- REST++ APIs for graph ingestion
- Idempotent upserts for reliability
- Docker for repeatable execution

---

## Problem Statement

The goal of this project is to design and implement a pipeline that:

1. Reads relational / tabular data (Iceberg-style schemas)
2. Maps tabular entities into a property graph
3. Creates TigerGraph schema programmatically
4. Loads vertices and edges using REST++ upserts
5. Supports repeatable, idempotent, batch ingestion
6. Can be executed locally or via Docker

This repository demonstrates **how Iceberg-style datasets can be modeled and ingested into TigerGraph reliably**.

---

## High-Level Architecture

Apache Iceberg (S3) --> Spark / Python (DataFrames / CSV) --> Relational → Graph Mapping --> TigerGraph REST++ APIs
(Vertex + Edge Upserts) --> TigerGraph Cloud (Savanna)

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
Using txn_id as a DISCRIMINATOR allows:

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

## Repository Structure

agivant/
- |-- spark_read_iceberg.py            # Spark-based Iceberg table reads via Unity Catalog
- |-- transform_to_graph.py            # Relational → graph transformation logic
- |-- spark_to_rest.py                 # Conversion of Spark rows to TigerGraph REST++ payloads
- |-- tigergraph_client.py             # TigerGraph REST++ upsert client (with dry-run support)
- |-- main.py                          # End-to-end driver (Databricks + local modes)
- |-- README.md                        # Documentation
- |-- Solution Proposal Document.pdf   # Architecture and tradeoff analysis              

---

## How the Prototype Works

1. `spark_read_iceberg.py`  
   Defines Spark logic to read Apache Iceberg tables using Unity Catalog identifiers.  
   This code is intended to run inside a Databricks workspace where Unity Catalog is available.

2. `transform_to_graph.py`  
   Applies schema-aware transformations to convert relational data into graph primitives:
   - Entity rows → TigerGraph vertices
   - Foreign-key relationships → TigerGraph edges

3. `spark_to_rest.py`  
   Converts transformed Spark DataFrames into TigerGraph REST++–compatible JSON payloads for vertices and edges.

4. `tigergraph_client.py`  
   Implements REST++ upsert calls to TigerGraph, with support for a dry-run mode that prints payloads when a TigerGraph instance is not available.

5. `main.py`  
   Orchestrates the end-to-end pipeline:
   - Runs Spark-based Iceberg ingestion in Databricks mode, or
   - Falls back to local mock data in local execution mode  
   
   In both cases, the pipeline generates TigerGraph REST++ upsert payloads and demonstrates ingestion behavior.



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


### Prerequisites
- Python 3.8 or later

### Run Command

```bash
python main.py
