# Reflection 5 in Module 5

In Module 5, we explored the real-world trade-offs between Normalization (3NF) and Denormalization using a factory maintenance dataset of 200,000 rows. We broke the flat schema with the three classic anomalies, decomposed it to 3NF, and benchmarked read query speeds, caching effects, update costs, and disk storage.

### Key Takeaways & Advice
The biggest takeaway for me is that **normalization is about write safety and integrity, while denormalization is an aggressive optimization for reading**. In our flat table, a basic fact like "cnc-01 is at Gütersloh" was copied thousands of times. Moving that machine to Bielefeld meant updating 4,000 separate rows in the flat table, compared to updating exactly 1 row in the 3NF `machine` table!

My advice:
1. Always normalize to 3NF first—it protects against insertion, update, and deletion anomalies.
2. Don't assume denormalization is automatically faster for SELECT queries—once caching comes into play, a normalized indexed schema can easily match or beat a wide denormalized table.
3. Only denormalize when you have a proven bottleneck at large scale (millions of rows) where multi-table joins exceed RAM cache, and do it through dedicated report tables rather than breaking your transactional model.

### Caching Effects on Normalized vs. Denormalized SELECT Speeds
One of the most surprising discoveries in our benchmarks was how **query speeds change dramatically once caching is involved**:
- **Cold Cache (First Run):** The denormalized table initially ran slightly faster (~43 ms vs. ~52 ms for normalized) because it avoided the 4-way join overhead on the first disk read.
- **Hot Cache (Second Run):** The normalized schema actually **beat the denormalized table** (~39 ms vs. ~48 ms)! 
- **Why this happens:** In 3NF, the dimension tables are tiny (`machine` has 50 rows, `part` has 40 rows; total size is ~7 KB). They fit completely inside the SQLite page cache and CPU L1/L2 cache. Looking up cached rows in RAM is virtually free. On the other hand, the denormalized table is wide and bloated with duplicated text strings (taking 37 MB on disk). Scanning through that large table thrashes the cache, requiring the CPU to stream far more bytes from memory.

### Factors Affecting SELECT Queries (Normalized vs. Denormalized, Indexed vs. Non-Indexed)
Comparing SELECT performance across different schema designs taught me that several distinct factors govern query execution:

1. **Row Width and Page I/O:** 
   - A normalized fact/junction table stores only compact integer foreign keys. More rows fit onto each 4 KB database page, allowing sequential scans to read fewer disk pages.
   - A denormalized flat table repeats wide text columns (`site`, `technician`, `part_name`) on every row, requiring the engine to read 2.5× more disk pages for the exact same query.

2. **Indexed vs. Non-Indexed Trade-Offs (Point Lookups vs. Large Scans):**
   - For **point lookups** (e.g. `WHERE machine_id = 'cnc-01'`), an index provides an order-of-magnitude win by navigating the B-tree directly to matching rows.
   - For **large aggregations** touching a significant percentage of rows (e.g. 30% of the dataset), an index can actually make queries **slower** than a full sequential scan! In our Round 4 experiment, dropping `ix_report_machine` actually made the dashboard query faster (dropped from ~45 ms down to ~25 ms). Walking an index B-tree requires two I/O seeks per matching row (one for the index leaf and one for the table rowid), whereas a non-indexed sequential scan reads continuous pages in order with high memory locality.

3. **Join Depth vs. Dimension Table Size:**
   - Joins are only expensive when joining two massive, uncached tables. When joining a large event table (`job_part`) to tiny dimension tables (`machine`, `part`), index-driven joins operate with near-zero overhead.

### What Was Good
Proving the three anomalies in Round 2 made database theory feel practical:
- *Update Anomaly:* Updating 4,000 rows just to move one CNC machine.
- *Insert Anomaly:* Being unable to add a new spare part to inventory without inventing a fake dummy job.
- *Delete Anomaly:* Deleting a completed repair job and accidentally erasing the only record of a spare part's price.

### What Was Difficult & Where I Struggled
The hardest part was keeping 2NF and 3NF distinct in practice:
- 2NF eliminates **partial key dependencies** (where an attribute depends on only part of a composite primary key, like `part_price` depending solely on `part_no` when the key is `(job_id, part_no)`).
- 3NF eliminates **transitive dependencies** (where a non-key attribute depends on another non-key attribute, like `job_id -> machine_id -> site`).
Visualizing these dependencies in the dependency diagrams helped solidify the difference.

**Yours Truly Trainn**
