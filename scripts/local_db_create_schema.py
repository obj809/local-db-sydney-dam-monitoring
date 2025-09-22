# scripts/local_db_create_schema.py

import os
import sys
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

SCHEMA_FILE = os.path.join(os.path.dirname(__file__), "../sql/schema.sql")


def load_env() -> None:
    dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
    if not os.path.exists(dotenv_path):
        print(f"Error: .env not found at {dotenv_path}")
        sys.exit(1)
    load_dotenv(dotenv_path)


def db_cfg() -> dict:
    cfg = {
        "host": os.getenv("LOCAL_DB_HOST", "127.0.0.1"),
        "port": int(os.getenv("LOCAL_DB_PORT", 3306)),
        "database": os.getenv("LOCAL_DB_NAME"),
        "user": os.getenv("LOCAL_DB_USER"),
        "password": os.getenv("LOCAL_DB_PASSWORD"),
    }
    missing = [k for k, v in cfg.items() if v in (None, "")]
    if missing:
        print(f"Error: Missing env vars: {', '.join(missing)}")
        sys.exit(1)
    return cfg


def connect(cfg: dict):
    try:
        conn = mysql.connector.connect(**cfg)
        if conn.is_connected():
            print(f"Connected to MySQL '{cfg['database']}'")
            return conn
        print("Error: could not connect to MySQL.")
        sys.exit(1)
    except Error as e:
        print(f"MySQL connection error: {e}")
        sys.exit(1)


def wipe_all_tables(conn) -> None:
    cur = conn.cursor()
    try:
        cur.execute("SET FOREIGN_KEY_CHECKS=0;")
        cur.execute("SHOW FULL TABLES WHERE Table_type='BASE TABLE';")
        tables = [r[0] for r in cur.fetchall()]
        if not tables:
            print("No tables to drop.")
        else:
            print(f"Dropping {len(tables)} table(s)…")
            for t in tables:
                cur.execute(f"DROP TABLE IF EXISTS `{t}`;")
                print(f"  - {t}")
        cur.execute("SET FOREIGN_KEY_CHECKS=1;")
        conn.commit()
        print("Wipe complete.")
    finally:
        cur.close()


def run_schema(conn, schema_path: str) -> None:
    if not os.path.exists(schema_path):
        print(f"Error: schema file not found at {schema_path}")
        sys.exit(1)

    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()

    cur = conn.cursor()
    try:
        cur.execute("SET FOREIGN_KEY_CHECKS=0;")
        print(f"Applying schema: {schema_path}")
        for _ in cur.execute(sql, multi=True):
            pass
        cur.execute("SET FOREIGN_KEY_CHECKS=1;")
        conn.commit()
        print("Schema applied successfully.")
    except Error as e:
        conn.rollback()
        print(f"Error applying schema: {e}")
        sys.exit(1)
    finally:
        cur.close()


def main() -> None:
    load_env()
    cfg = db_cfg()
    conn = connect(cfg)
    try:
        # Always wipe then apply
        wipe_all_tables(conn)
        run_schema(conn, SCHEMA_FILE)
    finally:
        if conn.is_connected():
            conn.close()
            print("MySQL connection closed.")


if __name__ == "__main__":
    main()
