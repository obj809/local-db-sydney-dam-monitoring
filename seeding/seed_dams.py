# seeding/seed_dams.py

import os
import sys
import mysql.connector
from dotenv import load_dotenv

DAMS = [
    ("203042", "Toonumbar Dam", 10814, -28.602383, 152.763769),
    ("210097", "Glenbawn Dam", 748827, -32.064304, 150.982007),
    ("210102", "Lostock Dam", 19736, -32.335999, 151.440793),
    ("210117", "Glennies Creek Dam", 282303, -32.339259, 151.286947),
    ("212205", "Nepean Dam", 67730, -34.335046, 150.617666),
    ("212211", "Avon Dam", 142230, -34.350932, 150.640500),
    ("212212", "Wingecarribee Reservoir", 29880, -34.540413, 150.498916),
    ("212220", "Cordeaux Dam", 93790, -34.336403, 150.745918),
    ("212232", "Cataract Dam", 97190, -34.265584, 150.803553),
    ("212243", "Warragamba Dam", 2064680, -33.891111, 150.591111),
    ("213210", "Woronora Dam", 69536, -34.109296, 150.936519),
    ("213240", "Prospect Reservoir", 33330, -33.832851, 150.890158),
    ("215212", "Tallowa Dam", 7500, -34.771563, 150.315266),
    ("215235", "Fitzroy Falls Reservoir", 9950, -34.645106, 150.487190),
    ("219027", "Brogo Dam", 8786, -36.476593, 149.722275),
    ("219033", "Cochrane Dam", 2700, -36.570300, 149.455400),
    ("410102", "Blowering Dam", 1604010, -35.515836, 148.254929),
    ("410131", "Burrinjuck Dam", 1024750, -35.014067, 148.643656),
    ("412010", "Lake Wyangala", 1217035, -33.931625, 149.010236),
    ("412106", "Carcoar Dam", 35917, -33.601561, 149.203153),
    ("412107", "Lake Cargelligo", 30163, -33.295281, 146.390692),
    ("412108", "Lake Brewster", 145369, -33.492387, 145.975896),
    ("416030", "Pindari Dam", 311500, -29.381739, 151.269225),
    ("418035", "Copeton Dam", 1345510, -29.904891, 150.989479),
    ("419041", "Keepit Dam", 418950, -30.819471, 150.516625),
    ("419069", "Chaffey Dam", 100509, -31.356884, 151.119117),
    ("419080", "Split Rock Dam", 393840, -30.537122, 150.674591),
    ("421078", "Burrendong Dam", 1154270, -32.688321, 149.157884),
    ("421148", "Windamere Dam", 366989, -32.782606, 149.815480),
    ("421189", "Oberon Dam", 45000, -33.724670, 149.866781),
    ("425022", "Lake Menindee", 629492, -32.343792, 142.328445),
    ("425023", "Lake Cawndilla", 631050, -32.475672, 142.229739),
    ("425046", "Lake Wetherell", 115759, -32.311286, 142.547640),
    ("425047", "Lake Tandure", 77419, -32.273230, 142.542400),
    ("42510036", "Lake Pamamaroo", 270001, -32.300000, 142.440000),
    ("42510037", "Lake Copi Hollow", 7729, -32.254265, 142.392175),
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
    c = cfg()
    conn = mysql.connector.connect(**c)
    cur = conn.cursor()
    sql = """
    INSERT INTO dams (dam_id, dam_name, full_volume, latitude, longitude)
    VALUES (%s,%s,%s,%s,%s)
    ON DUPLICATE KEY UPDATE
      dam_name=VALUES(dam_name),
      full_volume=VALUES(full_volume),
      latitude=VALUES(latitude),
      longitude=VALUES(longitude);
    """
    cur.executemany(sql, DAMS)
    conn.commit()
    print(f"seed_dams.py: upserted {cur.rowcount} rows")
    cur.close()
    conn.close()

if __name__ == "__main__":
    main()
