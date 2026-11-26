# Reflection 6a in Module 6a

In Module 6a, we addressed a classic database scaling problem: controlling wants to run historical analytical reports over two and a half years of data (2,000,000 rows), but running that heavy query against our operational SQLite database locks the single writer and stalls factory operations. The solution was decoupling the workload: keeping live writes in SQLite and moving historical analytics to DuckDB with Parquet.

### Key Takeaways & Advice
My biggest takeaway from this module is that **you must pick the database engine based on the shape of the work**. 
- SQLite is built for OLTP (handling individual rows, low-latency point lookups, and transactional write safety).
- DuckDB is built for OLAP (vectorized batch execution over millions of rows, reading columnar data where only the required columns are pulled into CPU cache).

My advice:
1. When reporting queries start blocking operational tables, export historical data into Parquet rather than forcing your transactional database to do heavy data warehousing.
2. Never use DuckDB for single-row web requests or sensor ingest loops—our boundary test proved SQLite is over 700× faster for individual `INSERT` statements.
3. Always verify data parity before benchmarking: if the row count and price sum between SQLite and Parquet don't match exactly, you're measuring data drift, not engine speed.

### What Was Good
The race between SQLite and DuckDB on 2,000,000 rows was incredible to watch:
- Dashboard query: SQLite took **2,751.0 ms**, while DuckDB finished in **24.8 ms** (**110.7× speedup**).
- Monthly report query: SQLite took **3,193.1 ms**, while DuckDB took **21.9 ms** (**145.7× speedup**).
- Storage footprint: The SQLite database was **112.7 MB**, while the dictionary-encoded Parquet file was only **2.32 MB** (48× smaller!). Testing Zstandard compression shrank it even further to **1.37 MB**.

The boundary test (`boundary.py`) was equally eye-opening: for 1,000 individual single-row inserts, SQLite took **2.06 ms**, while DuckDB took **1,482.91 ms**. DuckDB pays a noticeable per-statement compilation cost, which showed me exactly why DuckDB is the wrong engine for transactional logging.

### Learning from Classmates (The Trevors)
Reviewing the work and reflections of my classmates Trevor M Kiio and Trevor Fidel Nyongesa was really helpful:
- From **Trevor Kiio's reflection**, I learned to watch out for SQLite's strict `strftime` parameter ordering. SQLite requires `strftime('%Y-%m', done_on)` (format first, then date column). Calling it in reverse doesn't crash, but silently fails to group months correctly.
- From **Trevor Fidel's reflection**, I paid special attention to UTF-8 file encoding when exporting the CSV from SQLite so German characters like the umlaut in `Gütersloh` wouldn't trigger `Invalid unicode` decoding errors in DuckDB.
- Both of their benchmark results confirmed the same pattern: DuckDB dominates large historical aggregations using `HASH_GROUP_BY`, but SQLite dominates single-row inserts and point lookups.

### What Was Difficult & Where I Struggled
The hardest part was writing the automated refresh script (`refresh.py`) with `--check` verification. Ensuring that attaching SQLite directly inside DuckDB (`ATTACH 'history.db' AS sq (TYPE sqlite)`) and running the checksum verification worked reliably across multiple runs took some debugging, but seeing the SHA-256 hash match on repeated runs proved the pipeline was idempotent.

**Yours Truly Trainn**
