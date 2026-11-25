# Module 02: Pod Study Log

**Participant:** Trainn  
**Course:** HSBI Database Class — Module 02 Self/Pod Study  
**Topic:** Data Contracts & Reading Legacy Schemas  

---

## 1. References Used & Key Learnings (Task A)

| Source | Link | Concept Best Understood |
|---|---|---|
| **Course Module 02** | [02-data-contracts-and-legacy-schemas.md](file:///home/train/Downloads/hochschule/1.3/database/iotempire-teaching/full-classes/hsbi-databases-10d/modules/02-data-contracts-and-legacy-schemas.md) | How real-world database engineering is mostly reading and repairing flawed legacy schemas rather than greenfield design. |
| **Wikipedia: ER Model** | [Entity–relationship model](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model) | Clear distinction between entities (independent existence), attributes (descriptors), and relationships (links). |
| **Wikipedia: Crow's-foot** | [Notation & Cardinality](https://en.wikipedia.org/wiki/Entity%E2%80%93relationship_model#Cardinality_and_ordinality) | How mandatory vs. optional relationships are drawn with crossbars (`|`) and circles (`o`). |
| **Wikipedia: 1NF** | [First normal form](https://en.wikipedia.org/wiki/First_normal_form) | Why multi-value string packing (`'P-1001,P-1002'`) violates atomicity and breaks SQL joins. |
| **SQLite Docs** | [Foreign Key Support](https://sqlite.org/foreignkeys.html) | Why SQLite keeps foreign key enforcement turned OFF by default for legacy backward compatibility. |
| **Pydantic Docs** | [Pydantic v2](https://docs.pydantic.dev/) | Using code-first schemas and validators to reject dirty data at the API edge before reaching SQL. |

---

## 2. Things Googled

1. `sqlite foreign keys pragma default`: Learned that `PRAGMA foreign_keys = ON;` must be run on every new connection because it is a connection-level setting, not stored in the database file header.
2. `crow's foot notation mandatory many`: Verified that a mandatory many relationship is denoted by a crossbar followed by the three-pronged crow's foot (`|{`).
3. `sqlite glob syntax regex`: Understood how `installed NOT GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'` filters out non-ISO date entries in SQLite without full regex engines.
4. `surrogate key vs natural key performance`: Learned that 4-byte or 8-byte integer keys create smaller, faster B-Trees than variable-length strings, but unique constraints on natural keys are required for data validity.

---

## 3. Remarkable Things & Surprises

- **The Silent JOIN failure:** The biggest surprise was running `JOIN part ON part.part_no = maint_job.parts_used`. The query succeeds with code 0, but silently drops rows with multiple parts! In production, this would cause parts usage to be severely underreported without any visible database error.
- **Lexicographical comparison of numeric strings:** Running `SELECT * FROM part WHERE unit_price < '15'` returned `'12.50'`, but omitted `'9.90'`. Because the column is `TEXT`, the character `'9'` evaluates as greater than `'1'`. This means sorting by price in an e-commerce or inventory system produces completely wrong orders unless cast to `NUMERIC`.
- **Surrogate vs Natural Key compromise:** A surrogate key alone doesn't prevent duplicate parts from being entered into the database (e.g., entering `P-1003` twice with different IDs). A `UNIQUE` constraint on the natural key is mandatory.

---

## 4. LLM Q&A & Verification Against `legacy.db`

### Prompt 1: Natural Key vs. Surrogate Key
- **Prompt:** "Explain the difference between a natural key and a surrogate key, and give one real scenario where choosing the wrong one causes a data bug."
- **LLM Summary:** Natural keys come from real-world business data (e.g., serial number), while surrogate keys are auto-generated integer IDs. Using a natural key that changes (e.g., a customer email or a rebranded part number) causes cascading update failures across all foreign key tables.
- **Verification on `legacy.db`:** In `legacy.db`, `machine_name` (`cnc-01`) was used as a loose natural key. When machine names changed or someone entered an orphan name (`cnc-05`), maintenance records lost their association with actual physical machines.

### Prompt 2: Comma-Separated Values & 1NF
- **Prompt:** "A column holds a comma-separated list: `parts_used = 'P-1001,P-1002'`. Why does that violate 1NF, and what would the corrected schema look like?"
- **LLM Summary:** Violates atomicity. You cannot query with `WHERE part_no = 'P-1001'` using index scans; you must use slow `LIKE '%P-1001%'` which can falsely match `'P-10010'`.
- **Verification on `legacy.db`:** Verified directly: `SELECT * FROM maint_job WHERE parts_used = 'P-1001'` fails to find Job 1 even though Job 1 used `P-1001`.

---

## 5. From Words to Sketch (Task B)

### 1. 1:1 Relationship (Machine to Nameplate)
- **Rule:** Each machine has exactly one nameplate; each nameplate belongs to one machine.
- **Decision:** Place `machine_id` as the primary key of `nameplate` and make it a foreign key pointing to `machine(machine_id)`. Alternatively, if nameplate has no extra lifecycle, its attributes can reside directly on `machine`.

### 2. 1:n Relationship (Machine to Sensors)
- **Rule:** Each machine carries many sensors; each sensor is installed on one machine.
- **Decision:** Place `machine_id` as a foreign key on the "many" side: `sensor(sensor_id PK, machine_id FK, type, bus_address)`.

### 3. m:n Relationship (Work Orders to Parts)
- **Rule:** Work orders use many parts; each part is used in many work orders.
- **Decision:** Requires a junction table `work_order_part(work_order_id FK, part_no FK, quantity, PRIMARY KEY(work_order_id, part_no))`.

### 4. Entity vs. Attribute vs. Relationship
- **Scenario:** A maintenance job happens on one machine, performed by one technician on a date.
- **Decision:** `MaintenanceJob` is an **entity** (with its own `job_id` and date) that acts as a relationship binding `Machine` and `Technician`. `Technician` must be an entity, not just a name string, to track staff IDs, certifications, and avoid spelling inconsistencies.

### SQL Proof of Cardinality (1:n Machine to Sensor):
```sql
CREATE TABLE test_machine (
    machine_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE test_sensor (
    sensor_id INTEGER PRIMARY KEY,
    machine_id INTEGER NOT NULL REFERENCES test_machine(machine_id),
    model TEXT NOT NULL
);

INSERT INTO test_machine VALUES (1, 'Milling Center 1');
INSERT INTO test_sensor VALUES (101, 1, 'Vibration-X'), (102, 1, 'Temp-PT100');

-- Proof of 1:n: One machine has COUNT = 2 sensors
SELECT m.name, COUNT(s.sensor_id) AS sensor_count
FROM test_machine m
JOIN test_sensor s ON s.machine_id = m.machine_id
GROUP BY m.machine_id;
```

---

## 6. Agreed Learning (Pod Discussion — Task C)

During pod discussions with peers, we agreed upon the following core principles:
1. **Never trust documentation on legacy systems:** Always run `COUNT(*)` and `COUNT(DISTINCT col)` queries to discover actual cardinalities.
2. **A natural key without a `UNIQUE` constraint is just dirty text:** Declaring something as an intended identifier means nothing unless the database engine rejects duplicates.
3. **Multi-valued columns are technical debt:** Comma-separated values break query optimization, index usage, and foreign key integrity. A junction table is always the correct engineering solution.
4. **Defense in Depth:** Enforce data types and constraints in both the application layer (Pydantic models) and database schema (SQL constraints).
