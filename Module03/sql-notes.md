# SQL Notes & Pod Study Log — Module 03

**Student:** Trainn  
**Focus:** Relational Algebra, `EXPLAIN QUERY PLAN`, Index Tuning & Parameter Binding  

---

## 1. Relational Algebra to SQL Mapping

Relational algebra is the formal math; SQL is the execution syntax:

| Relational Algebra | SQL Keyword | What it Does |
|---|---|---|
| Selection ($\sigma$) | `WHERE` | Filters rows matching a predicate |
| Projection ($\pi$) | `SELECT` list | Picks specific columns |
| Join ($\bowtie$) | `JOIN ... ON` | Combines tables on a matching key |
| Union ($\cup$) / Difference ($-$) | `UNION` / `EXCEPT` | Set operations on matching schemas |
| Grouping ($\gamma$) | `GROUP BY` + aggregations | Groups rows and calculates summaries |
| Rename ($\rho$) | `AS` | Aliases table or column names |

---

## 2. The Six Clauses & Evaluation Order

SQL is written one way, but evaluated in a very different order:
1. `FROM` / `JOIN` — Grab the tables.
2. `WHERE` — Filter rows.
3. `GROUP BY` — Cluster into groups.
4. `HAVING` — Filter groups.
5. `SELECT` — Pick columns and evaluate aliases.
6. `ORDER BY` / `LIMIT` — Sort and truncate.

**Why this matters:** You cannot use an alias defined in `SELECT` inside a `WHERE` clause (e.g. `SELECT price * 1.19 AS gross ... WHERE gross > 100`) because `WHERE` runs long before `SELECT` exists.

---

## 3. Plan Safari (Task A on `legacy.db`)

Testing predictions before and after adding `ix_job_tech ON maint_job(technician)`:

| Query | Predicted Plan | Actual Plan (Before Index) | Actual Plan (After Index) | Why? |
|---|---|---|---|---|
| `WHERE technician = 'Beier'` | SCAN | SCAN `maint_job` | SEARCH `maint_job` USING INDEX `ix_job_tech` | Index directly looks up `'Beier'`. |
| `WHERE machine_name = 'cnc-02'` | SCAN | SCAN `machine` | SCAN `machine` | No index on `machine_name`, table scan is required. |
| `WHERE technician LIKE '%ei%'` | SCAN | SCAN `maint_job` | SCAN `maint_job` | Leading wildcard `%` prevents B-tree traversal. |

**Key Takeaway:** An index only helps if the query can navigate the B-tree from the root. A leading wildcard (`'%...'`) or wrapping the column in a function (`LOWER(col)`) forces a full table scan.

---

## 4. Curiosities & Questions

1. **Why does an index make an aggregate query slower?** In Task 2, adding `ix_orderline_order` made the dashboard query 4x slower (jumped from 260 ms to 1,120 ms). The planner switched from one fast linear scan of `order_line` to 60,000 individual index seeks.
2. **Covering Index win:** An index that includes all projected columns never touches the table. On a 100k row match, that saves 100,000 table seeks.
3. **Question posted to `#sql-questions`:** Does SQLite ever automatically build an ephemeral index in memory for a join if no index exists? (Answer: Yes, you will see `USE TEMP B-TREE FOR RIGHT-PART OF JOIN`).
