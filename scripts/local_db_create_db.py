# scripts/local_db_create_db.py

import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv


def load_environment_variables():
    """Load environment variables from the .env file."""
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    if not os.path.exists(dotenv_path):
        print(f"Error: .env file not found at {dotenv_path}")
        exit(1)
    load_dotenv(dotenv_path)


def get_db_config():
    """Retrieve database configuration from environment variables."""
    db_config = {
        'host': os.getenv('LOCAL_DB_HOST', 'localhost'),
        'port': int(os.getenv('LOCAL_DB_PORT', 3306)),
        'user': os.getenv('LOCAL_DB_USER'),
        'password': os.getenv('LOCAL_DB_PASSWORD'),
    }

    # Validate that required configurations are present
    missing = [key for key, value in db_config.items() if value is None]
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        exit(1)

    return db_config


def create_database(db_name, db_config):
    """Create a local MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password']
        )
        if connection.is_connected():
            print("Connected to MySQL Server.")

            # Create the database
            cursor = connection.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name};")
            print(f"Database '{db_name}' has been created or already exists.")
            cursor.close()

    except Error as e:
        print(f"Error while creating the database: {e}")

    finally:
        if 'connection' in locals() and connection.is_connected():
            connection.close()
            print("MySQL connection is closed.")


def main():
    """Main execution block to create the database."""
    load_environment_variables()

    db_config = get_db_config()
    db_name = os.getenv('LOCAL_DB_NAME', 'water_dashboard_nsw_local')

    create_database(db_name, db_config)


if __name__ == "__main__":
    main()
