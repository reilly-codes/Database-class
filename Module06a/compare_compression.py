"""Compare Parquet compression codecs (Snappy vs ZSTD) and query speeds."""
import time
from pathlib import Path
import duckdb

here = Path(__file__).parent
snappy_pq = here / "report_history.parquet"
zstd_pq = here / "report_zstd.parquet"

con = duckdb.connect()

# Generate zstd compressed parquet copy
con.execute(f"""
    COPY (SELECT * FROM read_parquet('{snappy_pq}'))
    TO '{zstd_pq}' (FORMAT parquet, COMPRESSION zstd);
""")

size_snappy = snappy_pq.stat().st_size
size_zstd = zstd_pq.stat().st_size

DASHBOARD = "SELECT machine_id, site, technician, SUM(part_price) FROM read_parquet('{src}') WHERE done_on >= '2026-01-01' GROUP BY machine_id, site, technician;"

# Warm-up and time Snappy
con.execute(DASHBOARD.format(src=str(snappy_pq))).fetchall()
t0 = time.perf_counter()
for _ in range(5):
    con.execute(DASHBOARD.format(src=str(snappy_pq))).fetchall()
t_snappy = ((time.perf_counter() - t0) / 5) * 1000

# Warm-up and time Zstandard
con.execute(DASHBOARD.format(src=str(zstd_pq))).fetchall()
t0 = time.perf_counter()
for _ in range(5):
    con.execute(DASHBOARD.format(src=str(zstd_pq))).fetchall()
t_zstd = ((time.perf_counter() - t0) / 5) * 1000

print(f"Codec       File Size       Ratio      Warm Query Time")
print("-" * 55)
print(f"Snappy      {size_snappy / 1e6:6.2f} MB       1.0x       {t_snappy:6.1f} ms")
print(f"Zstandard   {size_zstd / 1e6:6.2f} MB       {size_snappy / size_zstd:4.2f}x       {t_zstd:6.1f} ms")
