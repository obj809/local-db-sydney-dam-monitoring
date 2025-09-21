# File: scripts/local_export_mysql_to_excel.py
"""
Export all (or selected) MySQL tables to an Excel workbook in ../spreadsheets.
- Loads DB creds from .env (same style as your other scripts)
- One sheet per table
- Filename is date-stamped: water_dashboard_nsw_<YYYYMMDD_HHMM>.xlsx

Usage:
    python scripts/local_export_mysql_to_excel.py
    python scripts/local_export_mysql_to_excel.py --tables dams latest_data
"""

import os
import sys
import argparse
import datetime as dt
from typing import List, Optional, Dict

import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import pandas as pd


def load_environment_variables() -> None:
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    if not os.path.exists(dotenv_path):
        print(f"Error: .env file not found at {dotenv_path}")
        sys.exit(1)
    load_dotenv(dotenv_path)


def get_db_config() -> dict:
    db_config = {
        'host': os.getenv('LOCAL_DB_HOST', 'localhost'),
        'port': int(os.getenv('LOCAL_DB_PORT', 3306)),
        'database': os.getenv('LOCAL_DB_NAME'),
        'user': os.getenv('LOCAL_DB_USER'),
        'password': os.getenv('LOCAL_DB_PASSWORD'),
    }
    missing = [k for k, v in db_config.items() if v in (None, "")]
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        sys.exit(1)
    return db_config


def ensure_output_dir() -> str:
    out_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../spreadsheets'))
    os.makedirs(out_dir, exist_ok=True)
    return out_dir


def connect(db_config: dict):
    try:
        conn = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password'],
        )
        if conn.is_connected():
            return conn
        print("Error: Could not establish a MySQL connection.")
        sys.exit(1)
    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
        sys.exit(1)


def list_tables(conn, schema: str, only: Optional[List[str]] = None) -> List[str]:
    """Return base tables in the schema; if `only` is provided, filter to that set (case-insensitive)."""
    q = "SHOW FULL TABLES WHERE Table_type='BASE TABLE';"
    cur = conn.cursor()
    cur.execute(q)
    rows = cur.fetchall()
    cur.close()

    all_tables = sorted([r[0] for r in rows], key=str.lower)

    if only:
        wanted_lower = {t.lower() for t in only}
        filtered = [t for t in all_tables if t.lower() in wanted_lower]
        missing = [t for t in only if t.lower() not in {x.lower() for x in all_tables}]
        if missing:
            print(f"Warning: These tables were not found in '{schema}': {', '.join(missing)}")
        return filtered

    return all_tables


def _safe_sheet_name(name: str, existing: Dict[str, int]) -> str:
    """
    Make a valid, unique Excel sheet name:
    - Max 31 chars
    - Remove/replace invalid characters : \\ / ? * [ ]
    - Ensure uniqueness by appending a counter if needed
    """
    invalid = set(r':\/?*[]')
    cleaned = ''.join(ch for ch in name if ch not in invalid)
    cleaned = cleaned.strip()
    if not cleaned:
        cleaned = "Sheet"

    # Excel 31-char limit
    base = cleaned[:31]

    candidate = base
    # Ensure uniqueness
    while candidate.lower() in existing:
        existing[base.lower()] = existing.get(base.lower(), 0) + 1
        suffix = f"_{existing[base.lower()]}"
        candidate = (base[: (31 - len(suffix))] + suffix)
    existing[candidate.lower()] = 1
    return candidate


def export_tables_to_excel(conn, tables: List[str], out_path: str) -> None:
    print(f"Exporting {len(tables)} table(s) to: {out_path}")
    existing_sheet_names: Dict[str, int] = {}
    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
        for t in tables:
            try:
                df = pd.read_sql(f"SELECT * FROM `{t}`;", conn)
                sheet_name = _safe_sheet_name(t, existing_sheet_names)
                if df.empty:
                    # still create a sheet so you can see the structure
                    pd.DataFrame(columns=df.columns).to_excel(writer, index=False, sheet_name=sheet_name)
                    print(f"  ✓ {t} (0 rows)")
                else:
                    df.to_excel(writer, index=False, sheet_name=sheet_name)
                    print(f"  ✓ {t} ({len(df)} rows)")
            except Exception as e:
                print(f"  ✗ {t} — error: {e}")
    print("Done.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Export MySQL tables to Excel workbook")
    parser.add_argument(
        "--tables",
        nargs="*",
        help="Optional list of table names to export (default: all base tables).",
    )
    parser.add_argument(
        "--prefix",
        default="water_dashboard_nsw",
        help="Filename prefix for the Excel file (default: water_dashboard_nsw).",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    load_environment_variables()
    db_config = get_db_config()
    out_dir = ensure_output_dir()
    conn = connect(db_config)

    try:
        tables = list_tables(conn, db_config['database'], only=args.tables)
        if not tables:
            print("No tables to export.")
            sys.exit(0)

        stamp = dt.datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"{args.prefix}_{stamp}.xlsx"
        out_path = os.path.join(out_dir, filename)

        export_tables_to_excel(conn, tables, out_path)
        print(f"\nExcel created: {out_path}")
    finally:
        if conn.is_connected():
            conn.close()


if __name__ == "__main__":
    main()
