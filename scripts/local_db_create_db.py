# scripts/local_db_create_db.py

import os
import re
import sys
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

def load_environment_variables():
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    if not os.path.exists(dotenv_path):
        print(f"Error: .env file not found at {dotenv_path}")
        sys.exit(1)
    load_dotenv(dotenv_path)

def get_db_config():
    cfg = {
        'host': os.getenv('LOCAL_DB_HOST', 'localhost'),
        'port': int(os.getenv('LOCAL_DB_PORT', 3306)),
        'user': os.getenv('LOCAL_DB_USER'),
        'password': os.getenv('LOCAL_DB_PASSWORD'),
    }
    missing = [k for k, v in cfg.items() if v in (None, "")]
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        sys.exit(1)
    return cfg

def validate_db_name(name: str) -> None:
    # Basic safety: letters, numbers, _, $ only (common safe subset)
    if not name or not re.fullmatch(r'[A-Za-z0-9_$]+', name):
        print(f"Error: Invalid database name '{name}'. Use letters/numbers/_/$ only.")
        sys.exit(1)

def create_database(db_name: str, db_config: dict) -> None:
    charset = os.getenv('LOCAL_DB_CHARSET', 'utf8mb4')
    collation = os.getenv('LOCAL_DB_COLLATION', 'utf8mb4_0900_ai_ci')

    try:
        conn = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password']
        )
        if not conn.is_connected():
            print("Error: Could not connect to MySQL server.")
            sys.exit(1)

        print(f"Connected to MySQL at {db_config['host']}:{db_config['port']} as {db_config['user']}")

        cur = conn.cursor()
        # Note: identifiers can’t be parameterized; we validated the name above.
        cur.execute(
            f"CREATE DATABASE IF NOT EXISTS `{db_name}` "
            f"DEFAULT CHARACTER SET {charset} "
            f"DEFAULT COLLATE {collation};"
        )
        print(f"Database '{db_name}' ensured (charset={charset}, collation={collation}).")
        cur.close()
    except Error as e:
        print(f"Error while creating the database: {e}")
        sys.exit(1)
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()
            print("MySQL connection is closed.")

def main():
    load_environment_variables()
    cfg = get_db_config()

    db_name = os.getenv('LOCAL_DB_NAME', 'water_dashboard_nsw_local')
    validate_db_name(db_name)

    create_database(db_name, cfg)

if __name__ == "__main__":
    main()
