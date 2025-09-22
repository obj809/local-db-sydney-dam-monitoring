# seeding/seed_dam_group_members.py

import os
import mysql.connector
from dotenv import load_dotenv

MEMBERS = [
    ("sydney_dams","212232"), ("sydney_dams","212220"), ("sydney_dams","212211"),
    ("sydney_dams","212205"), ("sydney_dams","213210"), ("sydney_dams","213240"),
    ("sydney_dams","212212"), ("sydney_dams","215235"),
    ("popular_dams","212243"), ("popular_dams","212232"), ("popular_dams","212220"),
    ("popular_dams","212211"), ("popular_dams","212205"), ("popular_dams","213210"),
    ("popular_dams","215212"), ("popular_dams","213240"),
    ("large_dams","212243"), ("large_dams","410102"), ("large_dams","412010"),
    ("large_dams","418035"), ("large_dams","410131"), ("large_dams","421078"),
    ("large_dams","210097"), ("large_dams","419080"),
    ("small_dams","219033"), ("small_dams","215235"), ("small_dams","215212"),
    ("small_dams","42510037"), ("small_dams","219027"), ("small_dams","203042"),
    ("small_dams","210102"), ("small_dams","412107"),
    ("greatest_released","410102"), ("greatest_released","410131"),
    ("greatest_released","421078"), ("greatest_released","418035"),
    ("greatest_released","210117"), ("greatest_released","210097"),
    ("greatest_released","419041"), ("greatest_released","412010"),
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
        INSERT INTO dam_group_members (group_name, dam_id)
        VALUES (%s,%s)
        ON DUPLICATE KEY UPDATE group_name=VALUES(group_name), dam_id=VALUES(dam_id);
        """,
        MEMBERS,
    )
    conn.commit()
    print(f"seed_dam_group_members.py: upserted {cur.rowcount} rows")
    cur.close(); conn.close()

if __name__ == "__main__":
    main()
