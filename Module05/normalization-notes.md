# Database Normalization: A Comprehensive Guide

**Module 05 - Normalization vs. Denormalization**  
**Created:** November 5, 2026

---

## What is Database Normalization?

Database normalization is a systematic approach to organizing data in a relational database to reduce redundancy and improve data integrity. It involves decomposing tables into smaller, well-structured tables and defining relationships between them using foreign keys.

**The core goals of normalization are:**
- **Eliminate redundant data** - Store each fact exactly once
- **Ensure data dependencies make sense** - Only store related data together
- **Prevent update anomalies** - Avoid inconsistencies when inserting, updating, or deleting data
- **Improve data integrity** - Make the database structure logical and maintainable

Normalization follows a series of progressive rules called "normal forms." Each normal form builds upon the previous one, creating increasingly strict requirements that eliminate specific types of data anomalies. The most commonly used normal forms in practical database design are First Normal Form (1NF), Second Normal Form (2NF), and Third Normal Form (3NF).

---

## The Story: TechVarsity University Registration System

### Meet Sarah, the Database Administrator

Sarah works as a database administrator at TechVarsity University, a growing institution with 5,000 students. The university has been using a spreadsheet to track student enrollments, but it's becoming unmanageable. Students are complaining about incorrect grades appearing on their transcripts, and the registration office is spending hours fixing duplicate data.

The current spreadsheet looks like this:

| StudentID | StudentName | StudentEmail | Major | MajorDept | AdvisorName | AdvisorOffice | AdvisorPhone | Courses |
|---|---|---|---|---|---|---|---|---|
| S1001 | Emma Chen | emma.chen@techvarsity.edu | Computer Science | Engineering | Dr. James Wilson | ENG-301 | 555-0101 | CS101, CS201, MATH150 |
| S1002 | Marcus Johnson | marcus.j@techvarsity.edu | Data Science | Engineering | Dr. James Wilson | ENG-301 | 555-0101 | CS101, STAT200, MATH150 |
| S1003 | Aisha Patel | aisha.p@techvarsity.edu | Biology | Science | Dr. Sarah Kim | SCI-210 | 555-0202 | BIO101, CHEM101 |
| S1001 | Emma Chen | emma.chen@techvarsity.edu | Computer Science | Engineering | Dr. James Wilson | ENG-301 | 555-0101 | CS301 |

Sarah notices several problems immediately:
- **Emma appears twice** because she enrolled in a new course later
- **Dr. Wilson's office number is repeated** for every student he advises
- **Courses are stored as comma-separated lists**, making it impossible to track individual grades
- **If Dr. Wilson moves offices**, dozens of rows need updating

The university president asks Sarah to design a proper database. "We need to track students, their enrollments, courses, grades, instructors, and advisors efficiently," he says. Sarah knows this is a perfect use case for normalization.

Let's follow Sarah's journey as she normalizes this data from an unnormalized spreadsheet to a properly structured database in Third Normal Form (3NF).

---

## Step 0: Unnormalized Form (0NF) - The Problematic Spreadsheet

![Unnormalized Table](diagrams/0nf-table.png)

**Current State:**

| StudentID | StudentName | StudentEmail | Major | MajorDept | AdvisorName | AdvisorOffice | AdvisorPhone | Courses | Grades |
|---|---|---|---|---|---|---|---|---|---|
| S1001 | Emma Chen | emma.chen@techvarsity.edu | Computer Science | Engineering | Dr. James Wilson | ENG-301 | 555-0101 | CS101, CS201, MATH150 | A, B+, A- |
| S1002 | Marcus Johnson | marcus.j@techvarsity.edu | Data Science | Engineering | Dr. James Wilson | ENG-301 | 555-0101 | CS101, STAT200, MATH150 | A-, A, B |
| S1003 | Aisha Patel | aisha.p@techvarsity.edu | Biology | Science | Dr. Sarah Kim | SCI-210 | 555-0202 | BIO101, CHEM101 | B+, A |

### Problems Sarah Identifies:

1. **Repeating Groups:** The `Courses` and `Grades` columns contain multiple values
2. **Update Anomalies:**
   - Change Dr. Wilson's office → Must update multiple rows
   - Change Emma's major → Must update all her enrollment rows
3. **Insert Anomalies:**
   - Cannot add a new course without enrolling a student
   - Cannot add a new advisor without assigning students
4. **Delete Anomalies:**
   - If Aisha drops all courses, we lose Dr. Kim's information
   - If Marcus withdraws, we lose information about the Data Science major

**Sarah's goal:** Transform this into a clean, normalized database structure.

---

## Step 1: First Normal Form (1NF) - Atomic Values Only

### Rule: Eliminate Repeating Groups

**1NF Requirements:**
- Each column must contain only atomic (single) values
- No comma-separated lists or repeating groups
- Each row must be unique (requires a primary key)
- Order of rows doesn't matter

### Sarah's First Transformation

Sarah realizes the `Courses` and `Grades` columns violate 1NF because they contain multiple values. She restructures the data:

![First Normal Form](diagrams/1nf-table.png)

**StudentEnrollment (1NF):**

| StudentID | StudentName | StudentEmail | Major | MajorDept | AdvisorName | AdvisorOffice | AdvisorPhone | CourseID | CourseName | Grade |
|---|---|---|---|---|---|---|---|---|---|---|
| S1001 | Emma Chen | emma.chen@techvarsity.edu | Computer Science | Engineering | Dr. James Wilson | ENG-301 | 555-0101 | CS101 | Intro to Programming | A |
| S1001 | Emma Chen | emma.chen@techvarsity.edu | Computer Science | Engineering | Dr. James Wilson | ENG-301 | 555-0101 | CS201 | Data Structures | B+ |
| S1001 | Emma Chen | emma.chen@techvarsity.edu | Computer Science | Engineering | Dr. James Wilson | ENG-301 | 555-0101 | MATH150 | Calculus I | A- |
| S1002 | Marcus Johnson | marcus.j@techvarsity.edu | Data Science | Engineering | Dr. James Wilson | ENG-301 | 555-0101 | CS101 | Intro to Programming | A- |
| S1002 | Marcus Johnson | marcus.j@techvarsity.edu | Data Science | Engineering | Dr. James Wilson | ENG-301 | 555-0101 | STAT200 | Statistics | A |
| S1002 | Marcus Johnson | marcus.j@techvarsity.edu | Data Science | Engineering | Dr. James Wilson | ENG-301 | 555-0101 | MATH150 | Calculus I | B |
| S1003 | Aisha Patel | aisha.p@techvarsity.edu | Biology | Science | Dr. Sarah Kim | SCI-210 | 555-0202 | BIO101 | General Biology | B+ |
| S1003 | Aisha Patel | aisha.p@techvarsity.edu | Biology | Science | Dr. Sarah Kim | SCI-210 | 555-0202 | CHEM101 | General Chemistry | A |

**Primary Key:** `(StudentID, CourseID)` - The combination uniquely identifies each enrollment

### What Changed?

✅ **Fixed:** Repeating groups eliminated - each course enrollment is now a separate row  
✅ **Fixed:** All values are atomic - no more comma-separated lists  
✅ **Achieved:** Each row represents one student taking one course

### Remaining Problems:

❌ **Still has massive redundancy:** Emma's information (name, email, major, advisor) is repeated 3 times  
❌ **Update anomalies remain:** Changing Dr. Wilson's office still requires multiple updates  
❌ **Insert anomalies remain:** Still can't add a course without enrolling a student  
❌ **Partial dependencies exist:** Course name depends only on CourseID, not on the full key (StudentID, CourseID)

**Sarah's observation:** "We're in 1NF now, but we still have too much redundancy. Time for 2NF!"

---

## Step 2: Second Normal Form (2NF) - Eliminate Partial Dependencies

### Rule: Remove Attributes That Depend on Part of a Composite Key

**2NF Requirements:**
- Must already be in 1NF
- All non-key attributes must depend on the **entire** primary key, not just part of it
- Only applies to tables with composite primary keys

### Understanding Partial Dependencies

In the 1NF table, the primary key is `(StudentID, CourseID)`. Sarah identifies these functional dependencies:

| Left Side | Right Side | Dependency Type |
|---|---|---|
| `StudentID` → | `StudentName, StudentEmail, Major, MajorDept, AdvisorName, AdvisorOffice, AdvisorPhone` | **Partial dependency** (only part of key) |
| `CourseID` → | `CourseName` | **Partial dependency** (only part of key) |
| `(StudentID, CourseID)` → | `Grade` | **Full dependency** (entire key) |

**The problem:** Student information doesn't depend on which course they're taking, and course information doesn't depend on which student is enrolled. These are **partial dependencies** - they violate 2NF.

### Sarah's Second Transformation

Sarah decomposes the table into three tables, separating attributes based on what they depend on:

![Second Normal Form](diagrams/2nf-tables.png)

**Students Table:**

| StudentID (PK) | StudentName | StudentEmail | Major | MajorDept | AdvisorName | AdvisorOffice | AdvisorPhone |
|---|---|---|---|---|---|---|---|
| S1001 | Emma Chen | emma.chen@techvarsity.edu | Computer Science | Engineering | Dr. James Wilson | ENG-301 | 555-0101 |
| S1002 | Marcus Johnson | marcus.j@techvarsity.edu | Data Science | Engineering | Dr. James Wilson | ENG-301 | 555-0101 |
| S1003 | Aisha Patel | aisha.p@techvarsity.edu | Biology | Science | Dr. Sarah Kim | SCI-210 | 555-0202 |

**Courses Table:**

| CourseID (PK) | CourseName | Credits | Department |
|---|---|---|---|
| CS101 | Intro to Programming | 4 | Computer Science |
| CS201 | Data Structures | 4 | Computer Science |
| MATH150 | Calculus I | 4 | Mathematics |
| STAT200 | Statistics | 3 | Mathematics |
| BIO101 | General Biology | 4 | Biology |
| CHEM101 | General Chemistry | 4 | Chemistry |

**Enrollments Table:**

| StudentID (FK) | CourseID (FK) | Grade | Semester | Year |
|---|---|---|---|---|
| S1001 | CS101 | A | Fall | 2026 |
| S1001 | CS201 | B+ | Fall | 2026 |
| S1001 | MATH150 | A- | Fall | 2026 |
| S1002 | CS101 | A- | Fall | 2026 |
| S1002 | STAT200 | A | Fall | 2026 |
| S1002 | MATH150 | B | Fall | 2026 |
| S1003 | BIO101 | B+ | Fall | 2026 |
| S1003 | CHEM101 | A | Fall | 2026 |

**Primary Keys:**
- `Students`: `StudentID`
- `Courses`: `CourseID`
- `Enrollments`: `(StudentID, CourseID)` - composite primary key

### What Changed?

✅ **Fixed:** Partial dependencies eliminated - each table stores data dependent on its primary key  
✅ **Improved:** Emma's information stored once (not 3 times)  
✅ **Improved:** Course information stored once per course  
✅ **Fixed:** Can now add courses without enrolling students  
✅ **Fixed:** Can now add students without enrolling them in courses

### Remaining Problems:

❌ **Transitive dependencies:** `Major → MajorDept` and `AdvisorName → AdvisorOffice, AdvisorPhone`  
❌ **Update anomalies:** Changing Dr. Wilson's office still requires updating multiple student rows  
❌ **Delete anomalies:** If all Computer Science students graduate, we lose the fact that CS belongs to Engineering

**Sarah's observation:** "Better! But we still have redundancy in the Students table. Time for 3NF!"

---

## Step 3: Third Normal Form (3NF) - Eliminate Transitive Dependencies

### Rule: Remove Attributes That Depend on Other Non-Key Attributes

**3NF Requirements:**
- Must already be in 2NF
- No transitive dependencies: non-key attributes must depend **directly** on the primary key, not on other non-key attributes
- Mnemonic: "The key, the whole key, and nothing but the key"

### Understanding Transitive Dependencies

In the 2NF `Students` table, Sarah identifies these dependencies:

| Dependency | Type | Problem |
|---|---|---|
| `StudentID → Major` | Direct | ✅ OK |
| `Major → MajorDept` | Direct | ✅ OK independently |
| `StudentID → Major → MajorDept` | **Transitive** | ❌ Violates 3NF |
| `StudentID → AdvisorName` | Direct | ✅ OK |
| `AdvisorName → AdvisorOffice` | Direct | ✅ OK independently |
| `StudentID → AdvisorName → AdvisorOffice` | **Transitive** | ❌ Violates 3NF |

**The problem:** `MajorDept` depends on `Major`, not directly on `StudentID`. Similarly, `AdvisorOffice` and `AdvisorPhone` depend on `AdvisorName`, not directly on `StudentID`. These are **transitive dependencies**.

### Sarah's Final Transformation

Sarah decomposes the Students table further, creating separate tables for majors and advisors:

![Third Normal Form](diagrams/3nf-tables.png)

**Students Table (3NF):**

| StudentID (PK) | StudentName | StudentEmail | MajorID (FK) | AdvisorID (FK) |
|---|---|---|---|---|
| S1001 | Emma Chen | emma.chen@techvarsity.edu | CS | ADV001 |
| S1002 | Marcus Johnson | marcus.j@techvarsity.edu | DS | ADV001 |
| S1003 | Aisha Patel | aisha.p@techvarsity.edu | BIO | ADV002 |

**Majors Table:**

| MajorID (PK) | MajorName | DepartmentID (FK) |
|---|---|---|
| CS | Computer Science | DEPT-ENG |
| DS | Data Science | DEPT-ENG |
| BIO | Biology | DEPT-SCI |

**Departments Table:**

| DepartmentID (PK) | DepartmentName | Building | DeanName |
|---|---|---|---|
| DEPT-ENG | Engineering | Engineering Hall | Dr. Robert Martinez |
| DEPT-SCI | Science | Science Building | Dr. Linda Chen |
| DEPT-MATH | Mathematics | Math Tower | Dr. Ahmed Hassan |

**Advisors Table:**

| AdvisorID (PK) | AdvisorName | Office | Phone | DepartmentID (FK) |
|---|---|---|---|---|
| ADV001 | Dr. James Wilson | ENG-301 | 555-0101 | DEPT-ENG |
| ADV002 | Dr. Sarah Kim | SCI-210 | 555-0202 | DEPT-SCI |
| ADV003 | Dr. Michael Brown | MATH-105 | 555-0303 | DEPT-MATH |

**Courses Table (3NF):**

| CourseID (PK) | CourseName | Credits | DepartmentID (FK) | InstructorID (FK) |
|---|---|---|---|---|
| CS101 | Intro to Programming | 4 | DEPT-ENG | INST001 |
| CS201 | Data Structures | 4 | DEPT-ENG | INST001 |
| MATH150 | Calculus I | 4 | DEPT-MATH | INST002 |
| STAT200 | Statistics | 3 | DEPT-MATH | INST003 |
| BIO101 | General Biology | 4 | DEPT-SCI | INST004 |
| CHEM101 | General Chemistry | 4 | DEPT-SCI | INST005 |

**Instructors Table:**

| InstructorID (PK) | InstructorName | Office | Email | DepartmentID (FK) |
|---|---|---|---|---|
| INST001 | Prof. Alice Johnson | ENG-205 | alice.j@techvarsity.edu | DEPT-ENG |
| INST002 | Prof. David Lee | MATH-310 | david.l@techvarsity.edu | DEPT-MATH |
| INST003 | Prof. Maria Garcia | MATH-215 | maria.g@techvarsity.edu | DEPT-MATH |
| INST004 | Prof. John Smith | SCI-401 | john.s@techvarsity.edu | DEPT-SCI |
| INST005 | Prof. Emily Wang | SCI-302 | emily.w@techvarsity.edu | DEPT-SCI |

**Enrollments Table (3NF):**

| EnrollmentID (PK) | StudentID (FK) | CourseID (FK) | Grade | Semester | Year | Status |
|---|---|---|---|---|---|---|
| E001 | S1001 | CS101 | A | Fall | 2026 | Completed |
| E002 | S1001 | CS201 | B+ | Fall | 2026 | Completed |
| E003 | S1001 | MATH150 | A- | Fall | 2026 | Completed |
| E004 | S1002 | CS101 | A- | Fall | 2026 | Completed |
| E005 | S1002 | STAT200 | A | Fall | 2026 | Completed |
| E006 | S1002 | MATH150 | B | Fall | 2026 | Completed |
| E007 | S1003 | BIO101 | B+ | Fall | 2026 | Completed |
| E008 | S1003 | CHEM101 | A | Fall | 2026 | Completed |

### What Changed?

✅ **Fixed:** Transitive dependencies eliminated - each non-key attribute depends only on the primary key  
✅ **Fixed:** Dr. Wilson's office stored once in Advisors table  
✅ **Fixed:** Department information stored once in Departments table  
✅ **Fixed:** Major information stored once in Majors table  
✅ **Fixed:** Update Dr. Wilson's office → One row update  
✅ **Fixed:** Add new advisors without assigning students  
✅ **Fixed:** Delete all CS students → Department and Major information preserved  
✅ **Improved:** Can track instructors separately from courses  
✅ **Improved:** Can track departments as independent entities

### The Final 3NF Database Schema

![3NF ER Diagram](diagrams/3nf-er-diagram.png)

**Entities and Relationships:**
1. **Students** → enrolled in → **Enrollments** ← offered as ← **Courses**
2. **Students** → advised by → **Advisors**
3. **Students** → majoring in → **Majors** → belongs to → **Departments**
4. **Courses** → taught by → **Instructors**
5. **Courses** → offered by → **Departments**
6. **Advisors** → works in → **Departments**
7. **Instructors** → works in → **Departments**

---

## Sarah's Success: The Benefits of 3NF

Six months later, Sarah presents the results to the university president:

### Measured Improvements:

| Metric | Before (Spreadsheet) | After (3NF Database) | Improvement |
|---|---|---|---|
| **Storage redundancy** | Emma's data repeated 3× | Emma's data stored 1× | 67% reduction |
| **Update errors** | 23 errors/month | 0 errors/month | 100% elimination |
| **Time to update advisor office** | 45 minutes (manual) | 2 seconds (one query) | 99.9% faster |
| **Data inconsistencies** | 156 found | 0 found | 100% elimination |
| **Time to generate reports** | 2-3 hours | 30 seconds | 99.7% faster |

### Real-World Scenarios Solved:

1. **Scenario:** Dr. Wilson moves from ENG-301 to ENG-405
   - **Before:** Update 847 student records manually
   - **After:** Update 1 row in Advisors table
   
2. **Scenario:** Add new major "Cybersecurity" to Engineering Department
   - **Before:** Create entry with first enrolled student
   - **After:** Add one row to Majors table anytime

3. **Scenario:** Generate report of all students in Engineering majors
   - **Before:** Search entire spreadsheet, group manually
   - **After:** Simple JOIN query, instant results

4. **Scenario:** Delete graduated students
   - **Before:** Lose advisor and department information
   - **After:** All reference data preserved

---

## Summary: The Three Normal Forms

| Normal Form | Rule | What It Fixes | Real-World Example |
|---|---|---|---|
| **1NF** | Atomic values only; no repeating groups | Comma-separated lists and multi-valued columns | "CS101, CS201, MATH150" → separate rows for each course |
| **2NF** | No partial dependencies (non-key attributes must depend on entire key) | Redundancy from composite keys | Course name doesn't depend on which student enrolled |
| **3NF** | No transitive dependencies (non-key attributes depend only on the key) | Redundancy from non-key relationships | Advisor office depends on advisor, not on student |

### Mnemonic Device

**"The key, the whole key, and nothing but the key, so help me Codd"**  
(Referring to Edgar F. Codd, the inventor of the relational model)

- **The key:** Must have a primary key (1NF)
- **The whole key:** Depends on all of the primary key (2NF)
- **Nothing but the key:** Depends on nothing else but the primary key (3NF)

---

## Visualization: The Normalization Journey

```
0NF (Unnormalized)
┌─────────────────────────────────────────────────────┐
│ StudentID | Name | Courses (CS101,CS201,MATH150)  │
│ S1001     | Emma | Grades (A, B+, A-)             │ ← Repeating groups
└─────────────────────────────────────────────────────┘
                      ↓ Eliminate repeating groups
                      
1NF (First Normal Form)
┌─────────────────────────────────────────────────────┐
│ StudentID | Name | Major | CourseID | Grade        │
│ S1001     | Emma | CS    | CS101    | A            │ ← Emma repeated 3×
│ S1001     | Emma | CS    | CS201    | B+           │
│ S1001     | Emma | CS    | MATH150  | A-           │
└─────────────────────────────────────────────────────┘
                      ↓ Eliminate partial dependencies
                      
2NF (Second Normal Form)
┌─────────────────┐  ┌──────────────┐  ┌─────────────────┐
│ Students        │  │ Courses      │  │ Enrollments     │
│ StudentID | Name│  │ CourseID     │  │ StudentID       │
│ Major | Dept   │  │ Name         │  │ CourseID | Grade│
└─────────────────┘  └──────────────┘  └─────────────────┘
      ↓ Eliminate transitive dependencies
      
3NF (Third Normal Form)
┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐
│ Students     │  │ Courses      │  │ Enrollments  │  │ Majors       │
│ StudentID    │  │ CourseID     │  │ StudentID    │  │ MajorID      │
│ Name         │  │ Name         │  │ CourseID     │  │ Name         │
│ MajorID (FK) │  │ DepartmentID │  │ Grade        │  │ DepartmentID │
└──────────────┘  └──────────────┘  └──────────────┘  └──────────────┘
                                                               ↓
                                                        ┌──────────────┐
                                                        │ Departments  │
                                                        │ DepartmentID │
                                                        │ Name         │
                                                        └──────────────┘
Each fact stored exactly once!
```

---

## When NOT to Normalize: Denormalization

While normalization is generally good practice, there are situations where **denormalization** (deliberately violating normal forms) makes sense:

### Valid Reasons to Denormalize:

1. **Read-heavy analytics dashboards**
   - Joining 10 tables for every dashboard query is slow
   - Solution: Create a denormalized reporting table

2. **Performance-critical queries**
   - Real-time systems where milliseconds matter
   - Solution: Store frequently-accessed computed values

3. **Historical snapshots**
   - Need to preserve data as it was at a point in time
   - Solution: Denormalize to capture the complete state

### Sarah's Denormalization Example:

The university president wants a dashboard showing enrollment statistics updated every 30 seconds. Sarah creates a denormalized `EnrollmentSummary` table:

```sql
-- Denormalized for dashboard performance
CREATE TABLE EnrollmentSummary (
    StudentID,
    StudentName,
    MajorName,              -- Denormalized from Majors
    DepartmentName,         -- Denormalized from Departments
    TotalCredits,           -- Computed value
    CurrentGPA,             -- Computed value
    AdvisorName,            -- Denormalized from Advisors
    AdvisorOffice,          -- Denormalized from Advisors
    LastUpdated
);
```

**The key:** Sarah knows this is denormalized and maintains it with triggers or scheduled updates from the normalized tables.

---

## Key Takeaways

1. **Normalization reduces redundancy** but increases the number of tables
2. **Each normal form solves specific problems:**
   - 1NF: Eliminates repeating groups
   - 2NF: Eliminates partial dependencies
   - 3NF: Eliminates transitive dependencies
3. **3NF is the practical goal** for most transactional databases
4. **Denormalization is a deliberate choice** made for performance reasons, not an accident
5. **Normalization is about dependencies**, not just "splitting tables"

---

## References

1. **Codd, E. F. (1970).** "A Relational Model of Data for Large Shared Data Banks." *Communications of the ACM*, 13(6), 377-387.  
   https://dl.acm.org/doi/10.1145/362384.362685

2. **Microsoft Learn (2025).** "Database Normalization Description."  
   https://learn.microsoft.com/en-us/office/troubleshoot/access/database-normalization-description

3. **JanBask Training (2024).** "Normalization in SQL | 1NF, 2NF, 3NF and BCNF with Examples."  
   https://www.janbasktraining.com/blog/sql-database-normalization-1nf-2nf-3nf-4nf

4. **DataCamp (2024).** "Normalization in SQL (1NF - 5NF): A Beginner's Guide."  
   https://www.datacamp.com/tutorial/normalization-in-sql

5. **Relational Database Design (2024).** "Normalization in Database Design: 1NF, 2NF, 3NF Explained."  
   https://www.relationaldbdesign.com/database-analysis/module3/intro-normal-forms.php

6. **Red Gate Simple Talk (2020).** "Database Normal Forms Explained: 1NF, 2NF, 3NF, BCNF."  
   https://www.red-gate.com/simple-talk/databases/sql-server/t-sql-programming-sql-server/normalforms/

7. **Agile Data (2023).** "Introduction to Data Normalization: Database Design 101."  
   https://agiledata.org/essays/datanormalization.html

8. **Runestone Academy (2024).** "Normalization — A Practical Introduction to Databases."  
   https://runestone.academy/ns/books/published/practical_db/PART3_RELATIONAL_DATABASE_THEORY/03-normalization/normalization.html

9. **DEV Community (2024).** "Understanding Database Normalization: A Comprehensive Guide."  
   https://dev.to/adityapratapbh1/understanding-database-normalization-a-comprehensive-guide-b7f

10. **Viz-Note (2026).** "2NF Enrollment Example: Student-Course Database Guide."  
    https://www.viz-note.com/docs/database-normalization-step-by-step-guide/second-normal-form-2nf/2nf-enrollment-example

---

**Document History:**
- **Version 1.0** - November 5, 2026 - Initial comprehensive guide created
- **Author:** Database Class Module 05
- **Purpose:** Educational reference for normalization concepts (0NF → 3NF)
