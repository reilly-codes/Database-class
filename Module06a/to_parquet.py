"""Convert 200k CSV -> 2M-row Parquet using DuckDB and verify against SQLite."""
import sqlite3
from pathlib import Path
import duckdb

here = Path(__file__).parent
csv_path = here / "report_jobpart.csv"
parquet = here / "report_history.parquet"
db = here / "history.db"

con = duckdb.connect()

# Expand the 200k CSV 10x in DuckDB into Parquet
con.execute(f"""
    COPY (
      SELECT r.job_id + k * 1000000 AS job_id, r.machine_id, r.site,
             r.technician, r.part_no, r.part_price,
             CAST(r.done_on AS DATE) + CAST(k * 91 AS INTEGER) AS done_on
      FROM read_csv_auto('{csv_path}', header = true, encoding = 'utf-8') r,
           range(0, 10) t(k)
    ) TO '{parquet}' (FORMAT parquet)
""")

pq_rows = con.execute(f"SELECT COUNT(*) FROM read_parquet('{parquet}')").fetchone()[0]
pq_bytes = parquet.stat().st_size
pq_sum = con.execute(f"SELECT ROUND(SUM(part_price), 2) FROM read_parquet('{parquet}')").fetchone()[0]

sq_conn = sqlite3.connect(db)
sq_rows = sq_conn.execute("SELECT COUNT(*) FROM report_history;").fetchone()[0]
sq_bytes = db.stat().st_size
sq_sum = sq_conn.execute("SELECT ROUND(SUM(part_price), 2) FROM report_history;").fetchone()[0]

print(f"SQLite rows : {sq_rows:,} | SQLite sum : {sq_sum:,.2f} | Size : {sq_bytes / 1e6:.2f} MB")
print(f"Parquet rows: {pq_rows:,} | Parquet sum: {pq_sum:,.2f} | Size : {pq_bytes / 1e6:.2f} MB")
assert sq_rows == pq_rows, "Row count mismatch!"
assert sq_sum == pq_sum, "Price sum mismatch!"
print("Verification: PERFECT MATCH between SQLite and Parquet!")
