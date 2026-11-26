"""Refresh pipeline: Rebuild report_history.parquet from SQLite history.db with integrity checks."""
import argparse
import hashlib
import sqlite3
import sys
import time
from pathlib import Path
import duckdb

here = Path(__file__).parent
db_path = here / "history.db"
pq_path = here / "report_history.parquet"

def refresh(check: bool = False):
    t0 = time.perf_counter()
    if not db_path.exists():
        print(f"Error: {db_path} does not exist.", file=sys.stderr)
        sys.exit(1)

    con = duckdb.connect()
    # Export directly from SQLite attached database into Parquet
    con.execute(f"""
        ATTACH '{db_path}' AS sq (TYPE sqlite);
        COPY (SELECT * FROM sq.report_history) TO '{pq_path}' (FORMAT parquet);
    """)

    elapsed_ms = (time.perf_counter() - t0) * 1000
    pq_size = pq_path.stat().st_size
    pq_rows = con.execute(f"SELECT COUNT(*) FROM read_parquet('{pq_path}');").fetchone()[0]
    pq_sum = con.execute(f"SELECT ROUND(SUM(part_price), 2) FROM read_parquet('{pq_path}');").fetchone()[0]

    # Calculate file checksum
    h = hashlib.sha256()
    with open(pq_path, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    digest = h.hexdigest()[:12]

    if check:
        sq_conn = sqlite3.connect(db_path)
        sq_rows = sq_conn.execute("SELECT COUNT(*) FROM report_history;").fetchone()[0]
        sq_sum = sq_conn.execute("SELECT ROUND(SUM(part_price), 2) FROM report_history;").fetchone()[0]
        sq_conn.close()

        print(f"[CHECK] SQLite : rows={sq_rows:,}, sum={sq_sum:,.2f}")
        print(f"[CHECK] Parquet: rows={pq_rows:,}, sum={pq_sum:,.2f}")

        if sq_rows != pq_rows or sq_sum != pq_sum:
            print("[FAIL] Mismatch between SQLite source and Parquet export!", file=sys.stderr)
            sys.exit(1)
        print("[PASS] Integrity checks verified: exact match.")

    print(f"Refresh complete: rows={pq_rows:,} | size={pq_size / 1e6:.2f} MB | sha256={digest} | time={elapsed_ms:.1f} ms")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Refresh analytical Parquet export from SQLite.")
    parser.add_argument("--check", action="store_true", help="Verify row count and sum against SQLite source.")
    args = parser.parse_args()
    refresh(check=args.check)
