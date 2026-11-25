"""Benchmark index impacts and query plans on warehouse.db."""
import sqlite3
import statistics
import time
from pathlib import Path

DB = Path(__file__).with_name("warehouse.db")
conn = sqlite3.connect(DB)

DASHBOARD_QUERY = """
SELECT c.city, COUNT(DISTINCT c.customer_id) AS customers,
       SUM(ol.qty * p.price) AS revenue
FROM customer c
JOIN orders o     ON o.customer_id = c.customer_id
JOIN order_line ol ON ol.order_id = o.order_id
JOIN product p    ON p.product_id = ol.product_id
WHERE o.ordered_on >= '2025-01-01' AND o.ordered_on < '2026-01-01'
GROUP BY c.city
ORDER BY revenue DESC;
"""

DAY_QUERY = """
SELECT o.order_id, o.ordered_on, c.name
FROM orders o JOIN customer c ON c.customer_id = o.customer_id
WHERE o.ordered_on = '2026-02-14';
"""

FUNCTION_WRAP_QUERY = """
SELECT o.order_id, o.ordered_on, c.name
FROM orders o JOIN customer c ON c.customer_id = o.customer_id
WHERE date(o.ordered_on) = '2026-02-14';
"""

def get_plan(query: str):
    rows = conn.execute(f"EXPLAIN QUERY PLAN {query}").fetchall()
    return "\n".join(r[3] for r in rows)

def time_query(query: str, runs=3):
    times = []
    for _ in range(runs):
        t0 = time.perf_counter()
        conn.execute(query).fetchall()
        t1 = time.perf_counter()
        times.append((t1 - t0) * 1000.0) # in ms
    return statistics.median(times)

def reset_indexes():
    for idx in ["ix_orders_ordered_on", "ix_orderline_order", "ix_orderline_product"]:
        conn.execute(f"DROP INDEX IF EXISTS {idx}")
    conn.commit()

if __name__ == "__main__":
    print("=== 1. Baseline (No extra indexes) ===")
    reset_indexes()
    plan_base = get_plan(DASHBOARD_QUERY)
    t_dash_base = time_query(DASHBOARD_QUERY)
    plan_day_base = get_plan(DAY_QUERY)
    t_day_base = time_query(DAY_QUERY)
    print(f"Dashboard time: {t_dash_base:.2f} ms")
    print(f"Dashboard plan:\n{plan_base}\n")
    print(f"Single day time: {t_day_base:.2f} ms")
    print(f"Single day plan:\n{plan_day_base}\n")

    print("=== 2. Add ix_orders_ordered_on ===")
    conn.execute("CREATE INDEX ix_orders_ordered_on ON orders(ordered_on);")
    conn.commit()
    t_dash_idx1 = time_query(DASHBOARD_QUERY)
    plan_dash_idx1 = get_plan(DASHBOARD_QUERY)
    t_day_idx1 = time_query(DAY_QUERY)
    plan_day_idx1 = get_plan(DAY_QUERY)
    print(f"Dashboard time: {t_dash_idx1:.2f} ms")
    print(f"Dashboard plan:\n{plan_dash_idx1}\n")
    print(f"Single day time: {t_day_idx1:.2f} ms")
    print(f"Single day plan:\n{plan_day_idx1}\n")

    print("=== 3. Add ix_orderline_order ===")
    conn.execute("CREATE INDEX ix_orderline_order ON order_line(order_id);")
    conn.commit()
    t_dash_idx2 = time_query(DASHBOARD_QUERY)
    plan_dash_idx2 = get_plan(DASHBOARD_QUERY)
    print(f"Dashboard time: {t_dash_idx2:.2f} ms")
    print(f"Dashboard plan:\n{plan_dash_idx2}\n")

    print("=== 4. Add ix_orderline_product ===")
    conn.execute("CREATE INDEX ix_orderline_product ON order_line(product_id);")
    conn.commit()
    t_dash_idx3 = time_query(DASHBOARD_QUERY)
    plan_dash_idx3 = get_plan(DASHBOARD_QUERY)
    print(f"Dashboard time: {t_dash_idx3:.2f} ms")
    print(f"Dashboard plan:\n{plan_dash_idx3}\n")

    print("=== 5. Negative Result: Function Wrap defeating index ===")
    plan_wrap = get_plan(FUNCTION_WRAP_QUERY)
    t_wrap = time_query(FUNCTION_WRAP_QUERY)
    print(f"Wrap query time: {t_wrap:.2f} ms")
    print(f"Wrap query plan:\n{plan_wrap}\n")
