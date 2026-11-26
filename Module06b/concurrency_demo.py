"""Demonstrate concurrent write locking behavior."""
import sqlite3
import threading
import time
from pathlib import Path

here = Path(__file__).parent
db_path = here / "concurrency_test.db"

# Initialize test table
conn = sqlite3.connect(db_path)
conn.execute("DROP TABLE IF EXISTS machine;")
conn.execute("CREATE TABLE machine(machine_id INTEGER PRIMARY KEY, site TEXT, parts_produced INTEGER);")
conn.execute("INSERT INTO machine VALUES (1, 'guetersloh', 0);")
conn.commit()
conn.close()

def writer_1():
    con1 = sqlite3.connect(db_path, timeout=1.0)
    con1.execute("BEGIN IMMEDIATE;")
    con1.execute("UPDATE machine SET parts_produced = parts_produced + 1 WHERE machine_id = 1;")
    print("[Writer 1] Locked table and updated row. Sleeping for 2 seconds...")
    time.sleep(2.0)
    con1.commit()
    print("[Writer 1] Committed transaction.")
    con1.close()

def writer_2():
    time.sleep(0.5) # Wait for writer 1 to acquire lock
    con2 = sqlite3.connect(db_path, timeout=0.5)
    print("[Writer 2] Attempting to update the same row while Writer 1 holds lock...")
    try:
        con2.execute("BEGIN IMMEDIATE;")
        con2.execute("UPDATE machine SET parts_produced = parts_produced + 1 WHERE machine_id = 1;")
        con2.commit()
        print("[Writer 2] Succeeded!")
    except sqlite3.OperationalError as e:
        print(f"[Writer 2] Failed as expected: {e}")
    finally:
        con2.close()

if __name__ == "__main__":
    t1 = threading.Thread(target=writer_1)
    t2 = threading.Thread(target=writer_2)
    t1.start()
    t2.start()
    t1.join()
    t2.join()

    # Clean up test DB
    db_path.unlink(missing_ok=True)
