# Reflection 3 in Module 3

In this third module, we moved into writing complex queries and query optimization. The biggest theme was: "The LLM wrote it, it ran, but is it actually right, fast, and secure?"

### Key Takeaways & Advice
My biggest takeaway from this session is that **timing is just a symptom, but `EXPLAIN QUERY PLAN` is the real proof**. Before this class, I assumed that adding an index to a table always made queries faster. But during our benchmarking on `warehouse.db`, adding an index on `order_line(order_id)` actually made our dashboard query drop from 260 ms down to 1,120 ms—over 4 times slower! Looking at the plan showed that instead of doing one simple sequential scan across the table, SQLite was forced to do tens of thousands of separate B-tree seeks. 

My advice from what I learned:
1. Always profile with `EXPLAIN QUERY PLAN` before assuming an index helps.
2. Never trust an LLM's SQL blindly—always verify edge cases (like `DISTINCT` and date filtering) and check the plan.
3. Never use string formatting (`f"SELECT ... {user_input}"`) for queries. Always use parameter placeholders (`?`).

### What Was Good
I really enjoyed running the benchmark script (`bench.py`) and seeing the exact numbers. Seeing the single-day lookup query jump from 6.2 ms down to 0.27 ms (over 20x faster) when we added `ix_orders_ordered_on` was super satisfying. The SQL injection drill was also very clear—seeing `' OR '1'='1` dump the entire customer database in string formatting versus returning an empty list `[]` with parameter binding made the security risk crystal clear.

### What Was Difficult & Where I Struggled
The hardest part was understanding relational algebra notation ($\sigma, \pi, \bowtie, \gamma$) and translating it back and forth to SQL. Writing the written clause order vs the actual evaluation order was tricky at first, especially remembering why a column alias created in `SELECT` cannot be used in a `WHERE` clause.

### Interaction with AI
When I asked the LLM to write the revenue query for 2025, it produced a working query, but it initially suggested adding three separate indexes. When we benchmarked them one by one, only one actually helped the lookup query, one did nothing, and one made the main query 4x slower. This proved to me that AI models can write SQL syntax easily, but they don't profile execution plans on real data.

**Yours Truly Trainn**
