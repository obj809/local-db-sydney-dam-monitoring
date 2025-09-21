#!/usr/bin/env python3
# seeding/seed_latest_data.py
"""
Make sure every dam has a row in latest_data with simple fabricated values.

Rules (easy to read/change):
- percentage_full cycles: 92, 93, …, 100, 92, …
- inflow grows by +100 per dam (starting at 1000)
- release = 70% of inflow (rounded)
- storage_volume = percentage_full% of capacity
- if full_volume is NULL/0, we guess a capacity (200_000 + 10_000 * i)

This script:
1) SELECTs all dams (dam_id, dam_name, full_volume)
2) Builds rows using the rules above
3) UPSERTs into latest_data on (dam_id)
"""

import os
import datetime as dt
import mysql.connector
from dotenv import load_dotenv

def db_cfg():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    return dict(
        host=os.getenv("LOCAL_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("LOCAL_DB_PORT", "3306")),
        user=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        database=os.getenv("LOCAL_DB_NAME"),
    )

def main():
    cfg = db_cfg()
    today = dt.date.today().isoformat()

    conn = mysql.connector.connect(**cfg)
    cur = conn.cursor()

    # 1) fetch dams
    cur.execute("SELECT dam_id, dam_name, COALESCE(full_volume, 0) FROM dams ORDER BY dam_id;")
    dams = cur.fetchall()
    if not dams:
        print("seed_latest_data.py: No dams found. Seed 'dams' first.")
        cur.close(); conn.close(); return

    # 2) fabricate rows
    rows = []
    for i, (dam_id, dam_name, full_volume) in enumerate(dams):
        # percentage_full cycles 92..100 then repeats
        pct = 92 + (i % 9)  # 92–100
        # inflow is simple linear growth per dam
        inflow = 1000 + 100 * i
        release = round(inflow * 0.70, 3)

        # capacity fallback if missing
        cap = int(full_volume) if int(full_volume) > 0 else (200_000 + 10_000 * i)
        storage = round(cap * (pct / 100.0), 3)

        rows.append((dam_id, dam_name, today, storage, float(pct), float(inflow), release))

    # 3) upsert
    sql = """
    INSERT INTO latest_data
      (dam_id, dam_name, date, storage_volume, percentage_full, storage_inflow, storage_release)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
      dam_name=VALUES(dam_name),
      date=VALUES(date),
      storage_volume=VALUES(storage_volume),
      percentage_full=VALUES(percentage_full),
      storage_inflow=VALUES(storage_inflow),
      storage_release=VALUES(storage_release);
    """
    cur.executemany(sql, rows)
    conn.commit()

    print(f"seed_latest_data.py: upserted {cur.rowcount} row(s) for {len(rows)} dam(s).")
    cur.close(); conn.close()

if __name__ == "__main__":
    main()
