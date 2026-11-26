"""Race benchmark between SQLite and DuckDB on 2M rows."""
import sqlite3
import statistics
import time
from pathlib import Path
import duckdb

RUNS = 5

here = Path(__file__).parent
sq = sqlite3.connect(here / "history.db")
duck = duckdb.connect()
pq = str(here / "report_history.parquet")

DASHBOARD = """SELECT machine_id, site, technician, SUM(part_price) AS cost
FROM {src} WHERE done_on >= '2026-01-01'
GROUP BY machine_id, site, technician"""

# Use correct format for both: SQLite requires strftime(format, timestring)
SQLITE_MONTHLY = """SELECT strftime('%Y-%m', done_on) AS month, machine_id,
       COUNT(*) AS jobs, SUM(part_price) AS cost
FROM report_history GROUP BY month, machine_id ORDER BY month, machine_id"""

DUCKDB_MONTHLY = f"""SELECT strftime('%Y-%m', done_on) AS month, machine_id,
       COUNT(*) AS jobs, SUM(part_price) AS cost
FROM read_parquet('{pq}') GROUP BY month, machine_id ORDER BY month, machine_id"""

def timed_ms(fn):
    t0 = time.perf_counter()
    fn()
    return (time.perf_counter() - t0) * 1000

def spread(times):
    return f"{min(times):.1f}-{max(times):.1f}"

if __name__ == "__main__":
    queries = [
        ("dashboard",
         lambda: sq.execute(DASHBOARD.format(src="report_history")).fetchall(),
         lambda: duck.execute(DASHBOARD.format(src=f"read_parquet('{pq}')")).fetchall()),
        ("monthly",
         lambda: sq.execute(SQLITE_MONTHLY).fetchall(),
         lambda: duck.execute(DUCKDB_MONTHLY).fetchall()),
    ]

    print("Query        SQLite (ms) [spread]       DuckDB (ms) [spread]      Speedup")
    print("-" * 72)
    for name, run_sq, run_duck in queries:
        # Warm-up run (discarded)
        res_sq = run_sq()
        res_duck = run_duck()
        assert len(res_sq) == len(res_duck), f"Row count mismatch in {name}: {len(res_sq)} vs {len(res_duck)}"

        sq_times, duck_times = [], []
        for _ in range(RUNS):
            sq_times.append(timed_ms(run_sq))
            duck_times.append(timed_ms(run_duck))

        s = statistics.median(sq_times)
        d = statistics.median(duck_times)
        print(f"{name:11s} {s:8.1f} ms [{spread(sq_times):11s}]   {d:6.1f} ms [{spread(duck_times):11s}]   {s / d:6.1f}x")
