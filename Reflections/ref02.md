# Reflection 2 in Module 2

In this second module, we tackled conceptual database modeling from the perspective of an engineer inheriting an undocumented, broken legacy database. This was a completely different mindset from just writing queries—it was about forensic database analysis and data contracts.

### Key Takeaways & Advice
The biggest takeaway for me was that **you cannot trust column names or documentation in legacy schemas**. You have to prove everything with queries. When we ran the join between maintenance jobs and parts (`JOIN part ON part.part_no = maint_job.parts_used`), SQLite didn't crash or throw an error; it simply dropped all multi-part jobs in complete silence. That silence is far more dangerous than a runtime error because management or planning software could run for years undercounting parts without anyone noticing.

My advice to anyone doing data modeling:
1. Always decompose multi-valued lists into junction tables—never store comma-separated strings.
2. Use surrogate integer keys for fast joins and primary keys, but never forget to put a `UNIQUE` constraint on the natural key (like serial numbers).
3. Always turn on foreign key checks in SQLite (`PRAGMA foreign_keys = ON;`).

### What Was Good
I really enjoyed the detective work of finding the five integrity defects in `legacy.db`. Finding out that `'9.90' < '15'` evaluates to false because prices were stored as `TEXT` instead of `NUMERIC` was an eye-opener. It showed me how data types directly impact business logic. I also liked using `contract.py` with Pydantic and SQLAlchemy, seeing how an application data contract can reject invalid serial numbers (missing the `SN-` prefix) before the data ever reaches the database.

### What Was Difficult & Where I Struggled
The hardest part was understanding the exact placement of foreign keys in 1:1 and 1:n relationships and deciding how far to take inheritance. In mechatronics we often have sensors and actuators that inherit from a general device class, but modeling that in SQL with separate tables (Class Table Inheritance) versus a single table with a type column (Single Table Inheritance) required careful thinking about join costs versus schema cleanliness.

### Interactions & Pod Collaboration
During our pod discussions, comparing our ER sketches helped clarify the difference between business rules and true cardinalities (like why a car having 4 wheels is a validation check, not an architectural 1:4 cardinality). We verified our LLM prompts against our local `legacy.db` file and found that AI models frequently assume foreign keys exist simply because a column is named `machine_name`, which taught us to verify claims with SQL counts rather than taking generated models at face value.

**Yours Truly Trainn**
