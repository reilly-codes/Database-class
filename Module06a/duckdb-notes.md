# DuckDB Analytical Engine Notes — Module 06a

**Student:** Trainn  
**Focus:** Columnar Engines, Parquet Export, `EXPLAIN ANALYZE`, and Workload Boundaries  

---

## 1. Row-Oriented vs. Columnar Storage

- **SQLite (Row-Oriented / OLTP):** Stores whole rows contiguously on 4 KB B-tree pages. Ideal for point writes, single-row updates, and primary key lookups (`WHERE id = ?`). But an aggregation over 2 million rows requires loading every single unused column into memory.
- **DuckDB + Parquet (Columnar / OLAP):** Stores column values contiguously. A query aggregating `part_price` across machines reads only the specific column blocks required, completely ignoring other fields. Vectorized execution processes data in 2,048-element CPU SIMD batches.

---

## 2. Pod Discussion & Classmate Observations

Reviewing classmates' work and pod discussions:
- **Trevor Kiio's Observation on `strftime`:** SQLite strictly requires `strftime(format, timestring)` (e.g. `strftime('%Y-%m', done_on)`). Calling it in reverse silently returns `NULL` without erroring. Ensuring dialect-correct syntax was essential for matching result rows.
- **Trevor Fidel's Observation on Encoding & Boundaries:** Converting text from older tables required strict UTF-8 handling so special characters (`ü` in `Gütersloh`) wouldn't trigger parser aborts in DuckDB. In addition, the boundary test proved DuckDB pays a significant per-statement dispatch cost, making it unsuitable for live transaction loops.

---

## 3. Plan Analysis: `EXPLAIN QUERY PLAN` vs. `EXPLAIN ANALYZE`

- **SQLite `EXPLAIN QUERY PLAN`:**
  ```text
  SCAN report_history
  USE TEMP B-TREE FOR GROUP BY
  ```
  SQLite reads all 2M rows sequentially from disk and builds a temporary B-tree to cluster group keys, taking ~2.75 seconds.
- **DuckDB `EXPLAIN ANALYZE`:**
  ```text
  TABLE_SCAN (READ_PARQUET) -> PROJECTION -> HASH_GROUP_BY
  ```
  DuckDB projects only the 4 needed columns (`machine_id, site, technician, part_price`) and uses a vectorized hash table (`HASH_GROUP_BY`) to aggregate 2M rows into 350 groups in ~24 ms.
