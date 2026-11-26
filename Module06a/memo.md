# Engineering Memo: Analytical Reporting Architecture

**To:** Lea Winter (Controlling), Yasmin Kaya (Operations)  
**From:** Trainn (Database Engineering)  
**Date:** 2026-11-26  
**Subject:** Separation of Operational Ingestion from Historical Analytics  

### 1. Architectural Recommendation
We should immediately move the multi-quarter historical cost and machine analytics out of the operational SQLite database and into an immutable **Parquet** snapshot queried by **DuckDB**. Real-time transactional writes (new maintenance logs, machine telemetry, part replacements) will continue to live strictly in **SQLite (3NF)**.

### 2. Measured Evidence (2,000,000 Rows / 2.5 Years of Data)
Running analytics across 2 million rows in SQLite took **2,751.0 ms** for the plant dashboard and **3,193.1 ms** for the monthly report, blocking the single database writer and keeping controllers waiting. On the columnar Parquet file, DuckDB answered the exact same queries in **24.8 ms** (110× speedup) and **21.9 ms** (145× speedup), with zero locks on production tables. Furthermore, column-level dictionary encoding compressed the 2-million-row history from **112.7 MB** in SQLite down to **2.32 MB** in Parquet (a 48.5× storage reduction).

### 3. Ingestion & Refresh Strategy
The Parquet copy should be rebuilt via an automated nightly batch job (`refresh.py --check`) running at 02:00. If the refresh job silently fails or data becomes stale by 24 hours, financial reports will not reflect repairs completed during the current shift. However, for quarterly budgeting and machine reliability trends, a 24-hour staleness window is completely acceptable, whereas locking the production assembly line for 40-minute SQLite scans is unacceptable. Our refresh pipeline incorporates checksum and sum validation (`--check`) to fail loudly on data corruption.

### 4. Workloads That Must Stay in SQLite
We must **never** route live sensor ingestion, job dispatching, or technician point lookups through DuckDB. Our boundary benchmarks show SQLite is **721× faster** for single-row inserts (2.06 ms vs 1,482.91 ms for 1,000 writes) and **376× faster** for point lookups. DuckDB is an analytical columnar engine; SQLite remains our dedicated OLTP engine.
