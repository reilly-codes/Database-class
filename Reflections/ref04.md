# Reflection 4 in Module 4

In Module 4, we tackled data integrity at the edge—making the database itself reject invalid inputs without relying on a cloud server or application code to fix bad data.

### Key Takeaways & Advice
My biggest takeaway is that **integrity must be enforced where the data lives**. In edge computing (like a factory gateway logging machine metrics), network dropouts and sensor glitches happen constantly. If the database schema allows invalid types or impossible numbers, you end up with corrupt telemetry that is nearly impossible to clean up later.

My advice:
1. Always use `STRICT` mode in modern SQLite tables—it stops text from ending up in numeric columns.
2. Use generated virtual columns for derived measurements (`energy_j = value * interval_s`) so all readers calculate the same value consistently without storage waste.
3. Use `UPSERT` (`INSERT ... ON CONFLICT DO UPDATE`) for sensor data so replayed packets after network reconnects don't create duplicate records.

### What Was Good
I really liked seeing the constraints reject dirty rows with specific error messages. Seeing SQLite reject `9000` with `CHECK constraint failed` and reject `'hot'` with `cannot store TEXT value in REAL column` was very satisfying. The `UPSERT` test with `ingest.py` was also very cool—running the script twice on the same CSV kept the exact same row count (5 rows), proving idempotency.

### What Was Difficult & Where I Struggled
The trickiest concept was how SQLite handles access control (DCL) compared to client-server systems like PostgreSQL. Since SQLite has no `CREATE USER` or `GRANT`, access control depends on Unix file permissions (`chmod 444`) and connection modes (`file:edge.db?mode=ro`). Testing `DELETE FROM reading;` on `mode=ro` and seeing `attempt to write a readonly database` helped make that connection clear.

**Yours Truly Trainn**
