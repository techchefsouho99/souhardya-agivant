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

- Iceberg tables stored on S3
- Unity Catalog for schema discovery and access control
- Databricks Spark for reading and transforming data
- TigerGraph for storing vertices and edges


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

This prototype is intentionally minimal and demonstrates:

- Mocked Iceberg table rows (no real Iceberg dependency)
- Explicit schema-aware mapping logic
- Generation of TigerGraph-ready vertex and edge JSON

It does **not** include:
- Real Spark jobs
- Live Unity Catalog access
- A running TigerGraph instance

---

## Tradeoff Summary

### Batch vs Streaming

**Chosen approach: Batch ingestion**

Batch ingestion is preferred because:
- Iceberg is snapshot-oriented
- TigerGraph supports high-throughput bulk loading
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
- |-- mock_iceberg_data.py      # Mock Iceberg table rows
- |-- schema_mapping.py         # Relational → graph mapping logic
- |-- main.py                   # Driver script
- |-- README.md                 # Documentation                

---

## How the Prototype Works

1. `mock_iceberg_data.py` simulates rows from Iceberg tables:
   - users
   - products
   - transactions

2. `schema_mapping.py` converts relational rows into:
   - TigerGraph vertex representations
   - TigerGraph edge representations

3. `main.py` orchestrates the mapping and prints the results as JSON

In a production system, this logic would run inside a Spark job and output data to TigerGraph using:
- GSQL loading jobs (batch)
- REST++ APIs (incremental)

---

## How to Run the Prototype

### Prerequisites
- Python 3.8 or later

### Run Command

```bash
python main.py
