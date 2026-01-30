# Iceberg → TigerGraph Integration Prototype

## Overview

This repository contains a **lightweight prototype** demonstrating how data stored in **Apache Iceberg** tables can be ingested into **TigerGraph** using a **push-based, batch-oriented integration design**, with **Databricks Unity Catalog** acting as the metadata and governance layer.

The prototype focuses on **design clarity and feasibility**, not on deploying real infrastructure. It demonstrates how relational data from Iceberg can be transformed into graph-ready data structures suitable for ingestion into TigerGraph.

---

## Problem Statement

The goal of this project is to design a data integration pipeline that:

1. Discovers source schemas from Iceberg tables using Unity Catalog  
2. Maps relational/tabular data into graph structures (vertices and edges)  
3. Transfers data from Iceberg (on S3) into TigerGraph  
4. Supports repeatable and incremental graph updates  

This prototype illustrates the **core transformation logic** required to achieve this.

---

## High-Level Architecture

Data flows through the system as follows:

- **Apache Iceberg** stores versioned, snapshot-based tabular data  
- **Unity Catalog** provides centralized schema discovery and access control  
- **Spark** performs extraction and relational-to-graph transformation  
- **TigerGraph** ingests transformed data as graph vertices and edges  

---

## Graph Modeling Approach

The graph schema follows a **property graph model**:

### Vertices
- `User`: represents a user or account
- `Product`: represents a product or item

### Edges
- `PURCHASED`: represents a transactional relationship between a user and a product

Each transaction is modeled as a distinct edge, allowing:
- Many-to-many relationships
- Multiple transactions between the same user and product
- Rich traversal and analytics use cases

---

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
