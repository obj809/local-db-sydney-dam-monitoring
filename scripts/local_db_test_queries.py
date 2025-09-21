# scripts/local_db_test_queries.py
import os
import sys
import mysql.connector
from dotenv import load_dotenv
from mysql.connector import Error

SQL_PATH = os.path.join(os.path.dirname(__file__), "../sql/example_queries.sql")

def load_env():
    dotenv_path = os.path.join(os.path.dirname(__file__), "../.env")
    if not os.path.exists(dotenv_path):
        print(f"Error: .env not found at {dotenv_path}")
        sys.exit(1)
    load_dotenv(dotenv_path)

def cfg():
    return dict(
        host=os.getenv("LOCAL_DB_HOST", "127.0.0.1"),
        port=int(os.getenv("LOCAL_DB_PORT", "3306")),
        user=os.getenv("LOCAL_DB_USER"),
        password=os.getenv("LOCAL_DB_PASSWORD"),
        database=os.getenv("LOCAL_DB_NAME"),
    )

def read_queries(path: str):
    if not os.path.exists(path):
        print(f"Error: SQL file not found at {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        sql = f.read()

    # Split on semicolons but keep it simple: ignore empty and comment-only chunks
    chunks = [c.strip() for c in sql.split(";")]
    queries = []
    for c in chunks:
        if not c:
            continue
        # drop full-line comments
        lines = []
        for line in c.splitlines():
            l = line.strip()
            if l.startswith("--") or l == "":
                continue
            lines.append(line)
        q = "\n".join(lines).strip()
        if q:
            queries.append(q + ";")
    return queries

def main():
    load_env()
    cfg_dict = cfg()
    try:
        conn = mysql.connector.connect(**cfg_dict)
        print(f"\nConnected to MySQL, DB: {cfg_dict['database']}")
    except Error as e:
        print(f"Connection error: {e}")
        sys.exit(1)

    # Ensure @today is defined even if the SQL file forgot it
    bootstrap = ["SET @today = CURDATE();"]
    queries = bootstrap + read_queries(SQL_PATH)

    try:
        for idx, q in enumerate(queries, start=1):
            print(f"\n-- Query {idx} --")
            print(q.strip())
            # Use a NEW buffered cursor per statement -> avoids 'Unread result found'
            cur = conn.cursor(dictionary=True, buffered=True)
            try:
                cur.execute(q)
                # If it returns rows, fetch and print a few
                if cur.with_rows:
                    rows = cur.fetchall()
                    print(f"(ok, {len(rows)} row(s))")
                    # Print up to first 10 rows for brevity
                    for r in rows[:10]:
                        print(r)
                    if len(rows) > 10:
                        print(f"... ({len(rows) - 10} more rows)")
                else:
                    print(f"(ok, {cur.rowcount} row(s) affected)")
            except Error as e:
                print(f"(error) {e.msg}")
            finally:
                cur.close()
    finally:
        if conn.is_connected():
            conn.close()

if __name__ == "__main__":
    main()
