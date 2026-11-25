"""Idempotent CSV ingestion using SQLite UPSERT."""
import csv
import sqlite3
from pathlib import Path

DB = Path(__file__).with_name("edge.db")
CSV_FILE = Path(__file__).with_name("readings.csv")

UPSERT_SQL = """
INSERT INTO reading(sensor_id, ts, value, interval_s)
VALUES (?, ?, ?, ?)
ON CONFLICT(sensor_id, ts) DO UPDATE SET
    value = excluded.value,
    interval_s = excluded.interval_s;
"""

def ingest():
    conn = sqlite3.connect(DB)
    conn.execute("PRAGMA foreign_keys = ON;")
    # Ensure unique index exists for ON CONFLICT target
    conn.execute("CREATE UNIQUE INDEX IF NOT EXISTS ux_reading_sensor_ts ON reading(sensor_id, ts);")

    with open(CSV_FILE, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [(int(r["sensor_id"]), r["ts"], float(r["value"]), int(r["interval_s"])) for r in reader]

    conn.executemany(UPSERT_SQL, rows)
    conn.commit()

    count = conn.execute("SELECT COUNT(*) FROM reading;").fetchone()[0]
    conn.close()
    return count

if __name__ == "__main__":
    count_1 = ingest()
    print(f"Run 1 count: {count_1}")
    count_2 = ingest()
    print(f"Run 2 count: {count_2} (idempotent, no duplicates)")
