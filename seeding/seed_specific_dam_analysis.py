#!/usr/bin/env python3
# seeding/seed_specific_dam_analysis.py
"""
Upsert one specific_dam_analysis row per dam for the last day of the previous month.

Rules (easy to read/change):
- analysis_date = last day of previous month
- capacity = dams.full_volume if present, otherwise (200_000 + 10_000 * i)
- average volumes as % of capacity, with a tiny index-based wiggle:
    12m = (0.96 + wiggle) * capacity
     5y = (0.94 + wiggle) * capacity
    20y = (0.92 + wiggle) * capacity
  where wiggle = (i % 6) * 0.002   # up to +0.01
- average % full:
    12m = 96 - (i % 5)   (bounded to 85..100)
     5y = 94 - (i % 5)
    20y = 92 - (i % 5)
- inflow baseline per dam = 1200 + 50*i; 5y=0.97x, 20y=0.94x
- release = 70% of inflow set (12m/5y/20y respectively)
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

def last_day_prev_month() -> str:
    first_of_this_month = dt.date.today().replace(day=1)
    last_of_prev = first_of_this_month - dt.timedelta(days=1)
    return last_of_prev.isoformat()

def clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))

def main():
    cfg = db_cfg()
    analysis_date = last_day_prev_month()

    conn = mysql.connector.connect(**cfg)
    cur = conn.cursor()

    # Grab all dams so every dam gets an analysis row
    cur.execute("SELECT dam_id, COALESCE(full_volume, 0) FROM dams ORDER BY dam_id;")
    dams = cur.fetchall()
    if not dams:
        print("seed_specific_dam_analysis.py: No dams found. Seed 'dams' first.")
        cur.close(); conn.close(); return

    rows = []
    for i, (dam_id, full_vol) in enumerate(dams):
        # Choose a capacity (fallback if missing)
        capacity = int(full_vol) if int(full_vol) > 0 else (200_000 + 10_000 * i)

        # Small deterministic wiggle so numbers aren't identical
        wiggle = (i % 6) * 0.002  # up to +1%

        # Volumes as fraction of capacity
        v12 = round(capacity * (0.96 + wiggle), 3)
        v5  = round(capacity * (0.94 + wiggle), 3)
        v20 = round(capacity * (0.92 + wiggle), 3)

        # Percentages (bounded 85..100)
        p12 = clamp(96 - (i % 5), 85, 100)
        p5  = clamp(94 - (i % 5), 85, 100)
        p20 = clamp(92 - (i % 5), 85, 100)

        # Inflows and releases
        inflow12 = 1200 + 50 * i
        inflow5  = round(inflow12 * 0.97, 3)
        inflow20 = round(inflow12 * 0.94, 3)

        release12 = round(inflow12 * 0.70, 3)
        release5  = round(inflow5 * 0.70, 3)
        release20 = round(inflow20 * 0.70, 3)

        rows.append((
            dam_id, analysis_date,
            v12, v5, v20,
            float(p12), float(p5), float(p20),
            float(inflow12), float(inflow5), float(inflow20),
            float(release12), float(release5), float(release20),
        ))

    # Upsert by (dam_id, analysis_date)
    sql = """
    INSERT INTO specific_dam_analysis (
        dam_id, analysis_date,
        avg_storage_volume_12_months, avg_storage_volume_5_years, avg_storage_volume_20_years,
        avg_percentage_full_12_months, avg_percentage_full_5_years, avg_percentage_full_20_years,
        avg_storage_inflow_12_months, avg_storage_inflow_5_years, avg_storage_inflow_20_years,
        avg_storage_release_12_months, avg_storage_release_5_years, avg_storage_release_20_years
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
        avg_storage_volume_12_months=VALUES(avg_storage_volume_12_months),
        avg_storage_volume_5_years=VALUES(avg_storage_volume_5_years),
        avg_storage_volume_20_years=VALUES(avg_storage_volume_20_years),
        avg_percentage_full_12_months=VALUES(avg_percentage_full_12_months),
        avg_percentage_full_5_years=VALUES(avg_percentage_full_5_years),
        avg_percentage_full_20_years=VALUES(avg_percentage_full_20_years),
        avg_storage_inflow_12_months=VALUES(avg_storage_inflow_12_months),
        avg_storage_inflow_5_years=VALUES(avg_storage_inflow_5_years),
        avg_storage_inflow_20_years=VALUES(avg_storage_inflow_20_years),
        avg_storage_release_12_months=VALUES(avg_storage_release_12_months),
        avg_storage_release_5_years=VALUES(avg_storage_release_5_years),
        avg_storage_release_20_years=VALUES(avg_storage_release_20_years);
    """
    cur.executemany(sql, rows)
    conn.commit()

    print(f"seed_specific_dam_analysis.py: upserted {cur.rowcount} row(s) for {len(rows)} dam(s) on {analysis_date}.")
    cur.close(); conn.close()

if __name__ == "__main__":
    main()
