# seeding/seed_specific_dam_analysis.py

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

    cur.execute("SELECT dam_id, COALESCE(full_volume, 0) FROM dams ORDER BY dam_id;")
    dams = cur.fetchall()
    if not dams:
        print("seed_specific_dam_analysis.py: No dams found. Seed 'dams' first.")
        cur.close(); conn.close(); return

    rows = []
    for i, (dam_id, full_vol) in enumerate(dams):
        capacity = int(full_vol) if int(full_vol) > 0 else (200_000 + 10_000 * i)

        wiggle = (i % 6) * 0.002

        v12 = round(capacity * (0.96 + wiggle), 3)
        v5  = round(capacity * (0.94 + wiggle), 3)
        v20 = round(capacity * (0.92 + wiggle), 3)

        p12 = clamp(96 - (i % 5), 85, 100)
        p5  = clamp(94 - (i % 5), 85, 100)
        p20 = clamp(92 - (i % 5), 85, 100)

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
