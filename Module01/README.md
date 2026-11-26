# Module 1 — Introduction & Local-First Foundations

**Portfolio of:** Trainn  
**Class:** HSBI Database Class  

In this opening module, I set up the reproducible local toolchain (`uv`, Python, SQLite, DuckDB, Datasette), initialized the portfolio repository, explored embedded vs. client/server database architectures, and tested my first SQL queries with parameter binding and LLM query verification.

---

## 🎯 Learning Goals

| # | Official Learning Goal | Where Proven in Portfolio |
|---|---|---|
| **1** | Explain how this class works — the CBL/PBL philosophy, the portfolio-based **project work** assessment, and the "moving bar" of a first-time course. | [Task Inspirations & Class Structure](#task-inspirations) |
| **2** | Set up your personal GitHub portfolio from the course template, with a clean first commit and a `.gitignore` that keeps databases and secrets out of Git. | [Task Personal Profile](#task-personal-profile) & [Root `.gitignore`](../.gitignore) |
| **3** | Set up the entire toolchain reproducibly with **`uv`** — one fixed Python plus SQLite, DuckDB, Datasette, and more — on Windows, macOS, or Linux, and verify it. | [Root `pyproject.toml`](../pyproject.toml) & [Toolchain Evidence](pictures/README.md) |
| **4** | Explain — with a measurement, not a slide — the difference between an **embedded** database and a **client/server** database, and why most local apps should not run a server. | [Task What is IoT](#task-what-is-iot) & [Telemetry DB Size Proof](pictures/README.md#pictures-for-module-1) |
| **5** | Load real rows into SQLite and query them from Python using **bound parameters**. | [Ingestion Script (`load_telemetry.py`)](load_telemetry.py) & [Queries (`queries.sql`)](queries.sql) |
| **6** | Take a first LLM-generated query, run it, and begin the habit that defines this course: **verify before you trust**. | [Query Verification & Plan Proof](pictures/README.md) & [Reflection 1](/Reflections/ref01.md) |

---

## Task Inspirations

- Local first software architecture that eliminates unnecessary cloud dependencies
- Embedded IoT telemetry monitoring dashboards that run directly on local hardware without dedicated server infrastructure.

## Task Personal Profile

- **My Portfolio** : [Trainn](https://github.com/reilly-codes/Database-class/blob/main/README.md)

## Task What is IoT

The Internet of Things(IoT) refers to the collective network of physical objects embedded with sensors, software and network connectivity, allowing them to collect, process and exchange data with other devices over the internet.

Domains and included areas:

- Industrial Automation & Smart Manufacturing
- Smart Home & Edge Computing
- Smart Cities & Infrastructure
- Healthcare & Medical Devices


Commonly used (data) protocols:

- MQTT / CoAP (Lightweight messaging for edge sensors).
- HTTP REST / WebSockets (Telemetry transport and dashboards).

Typical devices (appliance or micro controller):

- Microcontrollers: ESP32, STM32.
- Single Board Computers: Raspberry Pi, industrial edge gateways.

Challenges:

- Network intermittent connectivity and bandwidth limits.
- Resource constraints (CPU, memory, storage wear) on edge devices.

## Reflection 1
[Reflection 1](/Reflections/ref01.md)

## Evidence
[Evidence](pictures/README.md)
