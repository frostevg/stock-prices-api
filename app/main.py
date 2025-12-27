from datetime import date
from typing import List, Optional

from fastapi import FastAPI, HTTPException

from app.db import get_connection
from app.schemas import Symbol

app = FastAPI(title="Stock Prices API", version="0.1.0")


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/symbols", response_model=List[Symbol])
def list_symbols():
    """
    Return all symbols from the stocks table.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute("SELECT symbol, company_name FROM stocks ORDER BY symbol;")
            rows = cur.fetchall()
        conn.close()
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# 1. LATEST PRICE FOR SYMBOL
# ===============================
@app.get("/prices/{symbol}/latest")
def latest_price(symbol: str):
    """
    Get the most recent close_price for a symbol.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT
                    s.symbol,
                    sp.close_price AS price,
                    sp.price_date AS date
                FROM stock_prices sp
                JOIN stocks s
                    ON sp.stock_id = s.stock_id
                WHERE s.symbol = %s
                ORDER BY sp.price_date DESC
                LIMIT 1;
                """,
                (symbol.upper(),),
            )
            row = cur.fetchone()
        conn.close()

        if not row:
            raise HTTPException(
                status_code=404,
                detail="Symbol not found or no price data",
            )
        return row

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# 2. PRICE HISTORY WITH RANGE
# ===============================
@app.get("/prices/history")
def price_history(
    symbol: str,
    start: Optional[date] = None,
    end: Optional[date] = None,
):
    """
    Get price history for a symbol, optionally filtered by date range.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            query = """
                SELECT
                    sp.price_date AS date,
                    sp.close_price AS price
                FROM stock_prices sp
                JOIN stocks s
                    ON sp.stock_id = s.stock_id
                WHERE s.symbol = %s
            """
            params = [symbol.upper()]

            if start:
                query += " AND sp.price_date >= %s"
                params.append(start)
            if end:
                query += " AND sp.price_date <= %s"
                params.append(end)

            query += " ORDER BY sp.price_date ASC;"

            cur.execute(query, tuple(params))
            rows = cur.fetchall()

        conn.close()
        return rows

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===============================
# 3. SUMMARY (MIN/MAX/AVG/LATEST)
# ===============================
@app.get("/summary/{symbol}")
def summary(symbol: str):
    """
    Get aggregated metrics: min, max, average and latest close_price.
    """
    try:
        conn = get_connection()
        with conn.cursor() as cur:
            # Aggregate stats
            cur.execute(
                """
                SELECT
                    MIN(sp.close_price) AS min_price,
                    MAX(sp.close_price) AS max_price,
                    AVG(sp.close_price) AS avg_price
                FROM stock_prices sp
                JOIN stocks s
                    ON sp.stock_id = s.stock_id
                WHERE s.symbol = %s;
                """,
                (symbol.upper(),),
            )
            stats = cur.fetchone()

            # Latest price
            cur.execute(
                """
                SELECT sp.close_price AS price
                FROM stock_prices sp
                JOIN stocks s
                    ON sp.stock_id = s.stock_id
                WHERE s.symbol = %s
                ORDER BY sp.price_date DESC
                LIMIT 1;
                """,
                (symbol.upper(),),
            )
            latest = cur.fetchone()

        conn.close()

        return {
            "symbol": symbol.upper(),
            "min": stats["min_price"],
            "max": stats["max_price"],
            "average": float(stats["avg_price"]) if stats["avg_price"] else None,
            "latest": latest["price"] if latest else None,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

