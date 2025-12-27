# Stock Prices API 📈

A FastAPI-based microservice that serves stock market data from Postgres.  
Built as part of my data engineering learning portfolio.

---

## Features

- FastAPI backend with REST endpoints
- PostgreSQL data storage
- Fetch latest stock price
- Price history for any symbol
- Summary stats (min/max/avg/latest)
- Fully documented via `/docs`

---

## Endpoints

| Method | Endpoint | Description |
|-------|----------|-------------|
| GET | `/health` | Check service status |
| GET | `/symbols` | List available stocks |
| GET | `/prices/{symbol}/latest` | Latest closing price |
| GET | `/prices/history?symbol=AAPL` | Full price history |
| GET | `/summary/AAPL` | Summary stats |

---

## Run locally

```bash
uvicorn app.main:app --reload

