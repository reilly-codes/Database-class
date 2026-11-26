"""Examine DuckDB EXPLAIN ANALYZE vs SQLite EXPLAIN QUERY PLAN on 2M rows."""
import sqlite3
from pathlib import Path
import duckdb

here = Path(__file__).parent
pq = here / "report_history.parquet"
db = here / "history.db"

# 1. DuckDB EXPLAIN ANALYZE
con = duckdb.connect()
plan = con.execute(f"""
    EXPLAIN ANALYZE
    SELECT machine_id, site, technician, SUM(part_price) AS cost
    FROM read_parquet('{pq}')
    WHERE done_on >= '2026-01-01'
    GROUP BY machine_id, site, technician
""").fetchall()[0][1]

# 2. SQLite EXPLAIN QUERY PLAN
sq_conn = sqlite3.connect(db)
sq_plan_rows = sq_conn.execute("""
    EXPLAIN QUERY PLAN
    SELECT machine_id, site, technician, SUM(part_price) AS cost
    FROM report_history
    WHERE done_on >= '2026-01-01'
    GROUP BY machine_id, site, technician
""").fetchall()
sq_plan = "\n".join(r[3] for r in sq_plan_rows)

print("=== DuckDB EXPLAIN ANALYZE ===")
print(plan)
print("\n=== SQLite EXPLAIN QUERY PLAN ===")
print(sq_plan)
