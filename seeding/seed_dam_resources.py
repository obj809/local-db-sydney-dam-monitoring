#!/usr/bin/env python3
# seeding/seed_dam_resources.py

import os
import datetime as dt
from dateutil.relativedelta import relativedelta
import mysql.connector
from dotenv import load_dotenv

# Generate 24 monthly points for each dam_id below (past 24 months)
DAM_FULL = {
    "212243": 2064680,  # Warragamba
    "212232": 97190,    # Cataract
    "212220": 93790,    # Cordeaux
    "410102": 1604010,  # Blowering
    "410131": 1024750,  # Burrinjuck
    "421078": 1154270,  # Burrendong
    "210097": 748827,   # Glenbawn
    "419080": 393840,   # Split Rock
}

def cfg():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    return dict(
        host=os.getenv("LOCAL_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("LOCAL_DB_PORT", "3306")),
        user=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        database=os.getenv("LOCAL_DB_NAME"),
    )

def month_ends(n_months=24):
    # last day of each month for the last n_months, ascending
    today = dt.date.today().replace(day=1)
    months = [(today - relativedelta(months=i)) for i in range(n_months, 0, -1)]
    # use first-of-month to simplify (matches your earlier sample style)
    return [d.isoformat() for d in months]

def main():
    conn = mysql.connector.connect(**cfg())
    cur = conn.cursor()

    dates = month_ends(24)

    # For idempotency without schema changes, delete only rows we’re about to re-insert.
    # This stays within the same table and avoids touching other tables.
    for dam_id in DAM_FULL:
        cur.execute(
            """
            DELETE FROM dam_resources
            WHERE dam_id=%s AND date BETWEEN %s AND %s;
            """,
            (dam_id, dates[0], dates[-1])
        )

    insert_sql = """
    INSERT INTO dam_resources
      (dam_id, date, storage_volume, percentage_full, storage_inflow, storage_release)
    VALUES (%s,%s,%s,%s,%s,%s);
    """

    rows = []
    for dam_id, full_vol in DAM_FULL.items():
        base = 92.0 + (hash(dam_id) % 40) * 0.1  # ~92.0–96.0%
        for i, d in enumerate(dates):
            # gentle seasonal wiggle
            pct = min(100.0, max(70.0, base + ((i % 12) - 6) * 0.3))
            storage = round(full_vol * (pct / 100.0), 3)
            inflow = round(1000 + (i * 20) + (hash(d) % 200) * 0.1, 3)
            release = round(inflow * (0.6 + (i % 5) * 0.05), 3)
            rows.append((dam_id, d, storage, pct, inflow, release))

    cur.executemany(insert_sql, rows)
    conn.commit()
    print(f"seed_dam_resources.py: inserted {cur.rowcount} rows")
    cur.close(); conn.close()

if __name__ == "__main__":
    main()
