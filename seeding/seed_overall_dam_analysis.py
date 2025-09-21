#!/usr/bin/env python3
# seeding/seed_overall_dam_analysis.py

import os
import datetime as dt
from dateutil.relativedelta import relativedelta
import mysql.connector
from dotenv import load_dotenv

def cfg():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    return dict(
        host=os.getenv("LOCAL_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("LOCAL_DB_PORT", "3306")),
        user=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        database=os.getenv("LOCAL_DB_NAME"),
    )

def last_day_prev_month():
    first = dt.date.today().replace(day=1)
    return (first - relativedelta(days=1)).isoformat()

def main():
    conn = mysql.connector.connect(**cfg())
    cur = conn.cursor()

    analysis_date = last_day_prev_month()

    sql = """
    INSERT INTO overall_dam_analysis (
        analysis_date,
        avg_storage_volume_12_months, avg_storage_volume_5_years, avg_storage_volume_20_years,
        avg_percentage_full_12_months, avg_percentage_full_5_years, avg_percentage_full_20_years,
        avg_storage_inflow_12_months, avg_storage_inflow_5_years, avg_storage_inflow_20_years,
        avg_storage_release_12_months, avg_storage_release_5_years, avg_storage_release_20_years
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
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

    # Plausible system-wide means (synthetic)
    v12 = 500000.000
    v5  = 480000.000
    v20 = 450000.000
    p12 = 98.50
    p5  = 96.00
    p20 = 94.00
    i12 = 1500.000
    i5  = 1400.000
    i20 = 1300.000
    r12 = 1100.000
    r5  = 1000.000
    r20 = 900.000

    cur.execute(sql, (analysis_date, v12, v5, v20, p12, p5, p20, i12, i5, i20, r12, r5, r20))
    conn.commit()
    print("seed_overall_dam_analysis.py: upserted 1 row")
    cur.close(); conn.close()

if __name__ == "__main__":
    main()
