# Data Integrity & Edge Triggers Notes — Module 04

**Student:** Trainn  
**Focus:** Constraints, `STRICT` Tables, Generated Columns, `UPSERT`, and Triggers  

---

## 1. The Three Layers of Integrity

1. **Entity Integrity**: Ensures every row is uniquely identifiable and complete (`PRIMARY KEY`, `NOT NULL`, `UNIQUE`).
2. **Referential Integrity**: Guarantees relationships point to valid parent records (`FOREIGN KEY` with `ON DELETE` / `ON UPDATE` actions). Note: SQLite requires `PRAGMA foreign_keys = ON;` per connection.
3. **Semantic / Domain Integrity**: Ensures stored values are physically meaningful and conform to business rules (`CHECK`, `STRICT` tables, generated columns, triggers).

---

## 2. Pod Study Acceptance Test

An unconstrained table `t(sensor_id INTEGER, metric TEXT, value REAL)` happily accepted:
- `(1, 'temp_c', 9000)` — physically impossible temperature.
- `(1, 'temp_c', 'hot')` — text inside a REAL column.
- `(2, 'bogus', -500)` — invalid metric and impossible value.

### Constrained Table Behavior:
Adding `STRICT`, `CHECK(metric IN (...))`, and `CHECK(value BETWEEN -273.15 AND 5000)` immediately caused SQLite to reject all junk rows:
- Text in REAL: `cannot store TEXT value in REAL column reading.value` (caught by `STRICT`).
- Out of bounds: `CHECK constraint failed: value >= -273.15 AND value <= 5000` (caught by `CHECK`).
- Invalid metric: `CHECK constraint failed: metric IN ('temp_c','vib_rms','spindle_load')`.

**`NULL` in `CHECK`:** In SQL, `CHECK` succeeds if the condition is `TRUE` or `UNKNOWN` (`NULL`). Therefore, `CHECK(value > 0)` permits `NULL` unless the column is explicitly marked `NOT NULL`!

---

## 3. Trigger Overhead & Placement

- `BEFORE INSERT` triggers run before row validation and storage. If a later constraint fails, changes made by a `BEFORE` trigger can leave phantom side effects.
- `AFTER INSERT` triggers guarantee the row has been validated and committed.
- Benchmarking 10,000 inserts showed:
  - Without trigger: 14.15 ms
  - With trigger: 17.57 ms (~24% overhead for evaluating `WHEN` condition and inserting alarm).
