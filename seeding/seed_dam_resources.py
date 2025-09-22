# seeding/seed_dam_resources.py

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

def month_starts(n_months=24):
    today = dt.date.today().replace(day=1)
    months = [(today - relativedelta(months=i)) for i in range(n_months, 0, -1)]
    return [d.isoformat() for d in months]

def main():
    conf = cfg()
    conn = mysql.connector.connect(**conf)
    cur = conn.cursor()

    cur.execute("SELECT dam_id, COALESCE(full_volume, 0) FROM dams ORDER BY dam_id;")
    dams = cur.fetchall()
    if not dams:
        print("seed_dam_resources.py: No dams found. Seed 'dams' first.")
        cur.close(); conn.close(); return

    dates = month_starts(24)

    for (dam_id, _) in dams:
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
    for i, (dam_id, full_vol) in enumerate(dams):
        capacity = int(full_vol) if int(full_vol) > 0 else (200_000 + 10_000 * i)
        base_pct = 90.0 + ((i % 20) * 0.5)
        for m, d in enumerate(dates):
            pct = min(100.0, max(60.0, base_pct + ((m % 12) - 6) * 0.35))
            storage = round(capacity * (pct / 100.0), 3)
            inflow = round(900 + (i * 15) + (m * 20), 3)
            release = round(inflow * 0.7, 3)
            rows.append((dam_id, d, storage, pct, inflow, release))

    cur.executemany(insert_sql, rows)
    conn.commit()
    print(f"seed_dam_resources.py: inserted {cur.rowcount} rows across {len(dams)} dams x {len(dates)} months.")
    cur.close(); conn.close()

if __name__ == "__main__":
    main()
