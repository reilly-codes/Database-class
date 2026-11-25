# Normalization Diagrams

This folder contains visual representations of the database normalization process from 0NF (Unnormalized) to 3NF (Third Normal Form) using the TechVarsity University case study.

## Diagram Files

### 0NF - Unnormalized Form
**File:** `0nf-table.mmd`  
**Shows:** The original problematic spreadsheet with repeating groups, comma-separated values, and all the data anomalies that normalization fixes.

**Key Problems Illustrated:**
- Repeating groups (courses and grades as comma-separated lists)
- Update anomalies (changing advisor office requires multiple updates)
- Insert anomalies (cannot add course without student)
- Delete anomalies (deleting student loses advisor information)

### 1NF - First Normal Form
**File:** `1nf-table.mmd`  
**Shows:** The first transformation where repeating groups are eliminated and all values are atomic.

**Key Features:**
- ✅ No repeating groups
- ✅ Atomic values (one value per cell)
- ❌ Still has massive redundancy
- ❌ Partial dependencies exist

### 2NF - Second Normal Form
**File:** `2nf-tables.mmd`  
**Shows:** Three separate tables (Students, Courses, Enrollments) after eliminating partial dependencies.

**Key Features:**
- ✅ No partial dependencies
- ✅ Student info stored once
- ✅ Course info stored once
- ❌ Transitive dependencies remain (Major → MajorDept, AdvisorName → Office)

### 3NF - Third Normal Form (Tables View)
**File:** `3nf-tables.mmd`  
**Shows:** Seven tables with all transitive dependencies eliminated.

**Tables:**
- Students (references Majors and Advisors)
- Majors (references Departments)
- Departments (independent)
- Advisors (references Departments)
- Courses (references Departments and Instructors)
- Instructors (references Departments)
- Enrollments (junction table)

### 3NF - Entity Relationship Diagram
**File:** `3nf-er-diagram.mmd`  
**Shows:** Complete ER diagram with all relationships and cardinalities in proper 3NF structure.

**Relationships:**
- Students ↔ Enrollments ↔ Courses (many-to-many)
- Students → Majors → Departments (many-to-one chains)
- Students → Advisors → Departments (many-to-one chains)
- Courses → Departments (many-to-one)
- Courses → Instructors → Departments (many-to-one chains)

---

## How to View These Diagrams

### Option 1: Mermaid Live Editor (Recommended)
1. Visit https://mermaid.live/
2. Copy the contents of any `.mmd` file
3. Paste into the editor
4. The diagram renders automatically
5. Export as PNG or SVG if needed

### Option 2: VS Code with Mermaid Extension
1. Install the "Markdown Preview Mermaid Support" extension
2. Open any `.mmd` file or the parent `normalization-notes.md`
3. Use the preview pane (Ctrl+Shift+V or Cmd+Shift+V)
4. Diagrams render inline

### Option 3: Command Line (if mermaid-cli is installed)
```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Generate PNG images
mmdc -i 0nf-table.mmd -o 0nf-table.png
mmdc -i 1nf-table.mmd -o 1nf-table.png
mmdc -i 2nf-tables.mmd -o 2nf-tables.png
mmdc -i 3nf-tables.mmd -o 3nf-tables.png
mmdc -i 3nf-er-diagram.mmd -o 3nf-er-diagram.png

# Or generate all at once
for file in *.mmd; do mmdc -i "$file" -o "${file%.mmd}.png"; done
```

### Option 4: GitHub/GitLab (Automatic Rendering)
If this repository is on GitHub or GitLab, Mermaid diagrams render automatically in markdown preview.

### Option 5: Obsidian or Notion
Both Obsidian and Notion support Mermaid syntax natively. Simply embed the diagram code in a code block with `mermaid` language tag.

---

## Understanding the Color Coding

### In Flow Diagrams:
- 🔴 **Red boxes** = Problems/anomalies (unnormalized state)
- 🟡 **Yellow boxes** = Partially normalized (still has issues)
- 🟢 **Green boxes** = Fully normalized (3NF achieved)

### In ER Diagrams:
- **Solid lines** = One-to-many relationships
- **Crow's foot notation** = Many side of relationship
- **PK** = Primary Key
- **FK** = Foreign Key

---

## Integration with normalization-notes.md

These diagrams are referenced in the main `normalization-notes.md` document at key points in the normalization journey:

- **Section: "Step 0: Unnormalized Form"** → `0nf-table.mmd`
- **Section: "Step 1: First Normal Form"** → `1nf-table.mmd`
- **Section: "Step 2: Second Normal Form"** → `2nf-tables.mmd`
- **Section: "Step 3: Third Normal Form"** → `3nf-tables.mmd` and `3nf-er-diagram.mmd`

---

## Quick Reference: Normal Form Rules

| Normal Form | Rule | Diagram Shows |
|---|---|---|
| **0NF** | Unnormalized data | All problems present |
| **1NF** | Atomic values, no repeating groups | Repeating groups eliminated |
| **2NF** | 1NF + no partial dependencies | Separate tables for different entities |
| **3NF** | 2NF + no transitive dependencies | All dependencies are key-based |

---

## Troubleshooting Diagram Rendering

### Issue: Diagram won't render in Mermaid Live Editor
**Solution:** Check for syntax errors. Common issues:
- Missing quotes around labels with spaces
- Unclosed subgraphs
- Invalid relationship syntax

### Issue: Diagram is too large/complex
**Solution:** 
- Zoom out in the viewer
- Export as SVG for better scalability
- Split into multiple smaller diagrams

### Issue: Colors not showing
**Solution:** Ensure your Mermaid renderer supports styling. The `style` statements at the end of each diagram define colors.

---

**Created:** November 5, 2026  
**Purpose:** Visual aids for understanding database normalization (Module 05)  
**Format:** Mermaid diagram syntax (.mmd files)  
**Related Document:** `../normalization-notes.md`
