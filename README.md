# Stock Prices API

A lightweight FastAPI microservice that exposes stock price data stored in PostgreSQL.  
This project is designed as a portfolio piece to demonstrate data engineering + backend API skills.

It is intended to be used together with my other project:

- **Stock Market Data Pipeline** – ETL pipeline that ingests daily prices into PostgreSQL.

---

## Features

- ✅ REST API built with **FastAPI**
- ✅ Connects to **PostgreSQL** (Docker container)
- ✅ Serves data originally ingested by an ETL pipeline
- ✅ Endpoints for:
  - Listing all available stock symbols
  - Getting latest price for a symbol
  - Querying historical prices (with optional date range)
  - Getting summary statistics (min / max / average / latest price)

---

## Architecture

**High-level flow:**

```text
ETL Pipeline (separate project) → PostgreSQL (stock_db) → FastAPI (this project) → Client / Dashboard

