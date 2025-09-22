# seeding/seed_dam_groups.py

import os
import mysql.connector
from dotenv import load_dotenv

GROUPS = [
    ("sydney_dams",),
    ("popular_dams",),
    ("large_dams",),
    ("small_dams",),
    ("greatest_released",),
]

def cfg():
    load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
    return dict(
        host=os.getenv("LOCAL_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("LOCAL_DB_PORT", "3306")),
        user=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        database=os.getenv("LOCAL_DB_NAME"),
    )

def main():
    conn = mysql.connector.connect(**cfg())
    cur = conn.cursor()
    cur.executemany(
        """
        INSERT INTO dam_groups (group_name)
        VALUES (%s)
        ON DUPLICATE KEY UPDATE group_name=VALUES(group_name);
        """,
        GROUPS,
    )
    conn.commit()
    print(f"seed_dam_groups.py: upserted {cur.rowcount} rows")
    cur.close(); conn.close()

if __name__ == "__main__":
    main()
