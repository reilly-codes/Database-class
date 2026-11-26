# Reflection 6b in Module 6b

In Module 6b, we brought everything together to answer the big architectural question: Kortmann has four different data shapes, so which database engine should handle which workload, and how do we defend that choice with numbers? We also tested the boundary between local embedded databases and remote servers, and experimented with schemaless JSON columns in SQLite.

### Key Takeaways & Advice
My biggest takeaway is that **polyglot persistence is about picking the right shape for the work, rather than trying to force one engine to do everything**. 
- High-frequency sensor ingestion belongs in SQLite (local ACID durability).
- Long-term multi-quarter analytics belong in DuckDB + Parquet (vectorized columnar scans).
- Evolving vendor hardware specs belong in a SQLite JSON column with expression indexes (flexibility without DDL migrations).

My advice:
1. Don't migrate a whole SQL table every time an external vendor adds an optional field—use a JSON column protected by `CHECK(json_valid(meta))`.
2. Be careful with expression indexes on JSON: SQLite matches the exact syntax tree. If you index `json_extract(meta, '$.vendor')`, querying with `meta ->> 'vendor'` silently skips the index and scans the entire table.
3. If forced to choose only one engine for a plant, pick SQLite for its versatility, but be prepared for analytical reports to slow down as history grows.

### What Was Good
Seeing how easy it is to handle semi-structured data in SQLite was a highlight. Being able to extract JSON values with `json_extract()`, unpack nested objects into key-value rows using `json_each()`, and speed up vendor queries with expression indexes showed that you don't need a heavy NoSQL database like MongoDB just to store variable metadata. 

The concurrency test was also very clear: seeing Writer 2 fail with `database is locked` while Writer 1 held an open transaction demonstrated how SQLite serializes writes at the file level, whereas a server like PostgreSQL uses row-level locking (MVCC).

### Learning from Classmates (The Trevors)
Reviewing the reflections from my classmates Trevor M Kiio and Trevor Fidel Nyongesa reinforced the key lessons:
- **From Trevor Kiio's reflection**, I paid close attention to the query plans for the 334 Fanuc devices. Both queries returned the exact same rows, but the plan difference between `json_extract` (index search) and `->>` (full table scan) showed that code generation from AI must always be checked with `EXPLAIN QUERY PLAN`. His observation about connection locks also matched my experience with transaction concurrency.
- **From Trevor Fidel's reflection**, I resonated with his point on polyglot persistence—that database selection is about matching the workload characteristics (OLTP vs OLAP vs Key-Value vs Document) rather than assuming one tool is universally better.
- A great question raised in Trevor Kiio's notes that I want to explore with our pod is: **At what point does an optional JSON attribute become important enough that it deserves to be promoted into its own dedicated relational column?** (My take: once you need foreign key constraints or need to join on it regularly).

### What Was Difficult & Where I Struggled
The hardest part was synthesizing all the course measurements into the one-page decision record and defending the "Only One Engine" choice. It forced me to weigh operational simplicity against query performance. Choosing SQLite as the single engine meant accepting that our two-year reporting queries will take minutes instead of milliseconds, but it guarantees that factory edge machines keep logging data even when the network drops.

**Yours Truly Trainn**
