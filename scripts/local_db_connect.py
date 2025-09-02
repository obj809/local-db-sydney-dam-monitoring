# scripts/local_db_connect.py

import os
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
    db_config = {
        'host': os.getenv('LOCAL_DB_HOST', 'localhost'),
        'port': int(os.getenv('LOCAL_DB_PORT', 3306)),
        'database': os.getenv('LOCAL_DB_NAME'),
        'user': os.getenv('LOCAL_DB_USER'),
        'password': os.getenv('LOCAL_DB_PASSWORD'),
    }

    missing = [key for key, value in db_config.items() if value is None]
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        sys.exit(1)

    return db_config


def test_connection(db_config):
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )

        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"Connected to MySQL Server version {db_info}")
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print(f"You're connected to database: {record[0]}")
            cursor.close()

    except Error as e:
        print(f"Error while connecting to MySQL: {e}")
    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection is closed")


def main():
    load_environment_variables()
    db_config = get_db_config()
    test_connection(db_config)


if __name__ == "__main__":
    main()
