"""Benchmark individual inserts and point lookups: where DuckDB is the WRONG engine."""
import sqlite3
import time
import duckdb

N = 1000

def test_sqlite():
    con = sqlite3.connect(":memory:")
    con.execute("CREATE TABLE s(id INTEGER PRIMARY KEY, k TEXT, v REAL);")
    
    # 1. Single-row inserts
    t0 = time.perf_counter()
    for i in range(N):
        con.execute("INSERT INTO s VALUES (?, ?, ?);", (i, f"k{i}", i * 1.5))
    con.commit()
    t_insert = (time.perf_counter() - t0) * 1000

    # 2. Point lookups
    t0 = time.perf_counter()
    for i in range(N):
        con.execute("SELECT v FROM s WHERE id = ?;", (i,)).fetchone()
    t_lookup = (time.perf_counter() - t0) * 1000

    # 3. Batch executemany
    con.execute("DELETE FROM s;")
    rows = [(i, f"k{i}", i * 1.5) for i in range(N)]
    t0 = time.perf_counter()
    con.executemany("INSERT INTO s VALUES (?, ?, ?);", rows)
    con.commit()
    t_batch = (time.perf_counter() - t0) * 1000

    return t_insert, t_lookup, t_batch

def test_duckdb():
    con = duckdb.connect()
    con.execute("CREATE TABLE s(id INTEGER PRIMARY KEY, k TEXT, v DOUBLE);")

    # 1. Single-row inserts
    t0 = time.perf_counter()
    for i in range(N):
        con.execute("INSERT INTO s VALUES (?, ?, ?);", (i, f"k{i}", i * 1.5))
    t_insert = (time.perf_counter() - t0) * 1000

    # 2. Point lookups
    t0 = time.perf_counter()
    for i in range(N):
        con.execute("SELECT v FROM s WHERE id = ?;", (i,)).fetchone()
    t_lookup = (time.perf_counter() - t0) * 1000

    # 3. Batch executemany
    con.execute("DELETE FROM s;")
    rows = [(i, f"k{i}", i * 1.5) for i in range(N)]
    t0 = time.perf_counter()
    con.executemany("INSERT INTO s VALUES (?, ?, ?);", rows)
    t_batch = (time.perf_counter() - t0) * 1000

    return t_insert, t_lookup, t_batch

if __name__ == "__main__":
    sq_ins, sq_look, sq_batch = test_sqlite()
    dk_ins, dk_look, dk_batch = test_duckdb()

    print(f"Operation ({N} calls)          SQLite          DuckDB         Winner")
    print("-" * 65)
    print(f"Single-row INSERTs         {sq_ins:8.2f} ms     {dk_ins:8.2f} ms     SQLite ({dk_ins / sq_ins:.1f}x faster)")
    print(f"Single-row point SELECTs   {sq_look:8.2f} ms     {dk_look:8.2f} ms     SQLite ({dk_look / sq_look:.1f}x faster)")
    print(f"Batch executemany INSERTs  {sq_batch:8.2f} ms     {dk_batch:8.2f} ms     SQLite ({dk_batch / sq_batch:.1f}x faster)")
