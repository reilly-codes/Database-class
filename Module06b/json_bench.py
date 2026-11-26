"""A JSON column in SQLite: store flexibly, query precisely, index deliberately."""
import json
import sqlite3
from pathlib import Path

here = Path(__file__).parent
con = sqlite3.connect(here / "polyglot.db")

con.executescript("""
DROP TABLE IF EXISTS device;
CREATE TABLE device(
    device_id INTEGER PRIMARY KEY,
    name      TEXT NOT NULL,
    meta      TEXT NOT NULL CHECK (json_valid(meta))   -- it *is* JSON, enforced
) STRICT;
""")

rows = [
    ("cnc-01",    '{"vendor":"Siemens","firmware":"4.2","calibrated":"2026-01-10"}'),
    ("cnc-02",    '{"vendor":"Fanuc","firmware":"3.9"}'),
    ("molder-07", '{"vendor":"Arburg","firmware":"8.1","calibrated":"2025-11-02","nozzle_mm":2.5}'),
]
for i in range(4, 1001):
    meta = json.dumps({
        "vendor": ("Siemens", "Fanuc", "Arburg")[i % 3],
        "firmware": f"{i % 5}.{i % 10}",
    })
    rows.append((f"device-{i:04d}", meta))
con.executemany("INSERT INTO device(name, meta) VALUES (?, ?)", rows)

print("-- 1. Path extraction via json_extract (first 3 rows):")
for row in con.execute("SELECT name, json_extract(meta, '$.vendor') FROM device LIMIT 3"):
    print(row)

print("\n-- 2. Arrow shorthand ->> (first 3 rows):")
for row in con.execute("SELECT name, meta ->> '$.firmware' FROM device LIMIT 3"):
    print(row)

print("\n-- 3. Unpacking JSON object into key/value rows via json_each (cnc-01):")
for row in con.execute(
        "SELECT d.name, j.key, j.value FROM device d, json_each(d.meta) j "
        "WHERE d.name = 'cnc-01'"):
    print(row)

print("\n-- 4. Creating expression index on json_extract:")
con.executescript("""
CREATE INDEX ix_device_vendor ON device(json_extract(meta, '$.vendor'));
""")

plan_indexed = con.execute(
    "EXPLAIN QUERY PLAN SELECT name FROM device "
    "WHERE json_extract(meta, '$.vendor') = 'Fanuc'").fetchall()
print("Plan with json_extract (matches index):")
for step in plan_indexed:
    print("  ", step[3])

plan_arrow = con.execute(
    "EXPLAIN QUERY PLAN SELECT name FROM device "
    "WHERE meta ->> 'vendor' = 'Fanuc'").fetchall()
print("\nPlan with ->> shorthand (breaks index):")
for step in plan_arrow:
    print("  ", step[3])
