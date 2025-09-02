# scripts/local_db_seed_data.py

import os
import mysql.connector
from dotenv import load_dotenv


def load_environment_variables():
    dotenv_path = os.path.join(os.path.dirname(__file__), '../.env')
    if not os.path.exists(dotenv_path):
        print(f"Error: .env file not found at {dotenv_path}")
        exit(1)
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
        exit(1)

    return db_config


def connect_to_database(db_config):
    try:
        connection = mysql.connector.connect(
            host=db_config['host'],
            port=db_config['port'],
            database=db_config['database'],
            user=db_config['user'],
            password=db_config['password']
        )
        print("Connection to the local database was successful!")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def seed_database_from_file(connection, sql_file_path):
    cursor = connection.cursor()
    try:
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()

        sql_commands = sql_script.split(';')
        for command in sql_commands:
            if command.strip():
                cursor.execute(command)
        
        connection.commit()
        print(f"Data from {sql_file_path} has been seeded into the database successfully!")

    except FileNotFoundError:
        print(f"Error: The file {sql_file_path} does not exist.")
    except mysql.connector.Error as err:
        print(f"Error while seeding data: {err}")
    finally:
        cursor.close()


def main():

    load_environment_variables()

    db_config = get_db_config()

    db_connection = connect_to_database(db_config)

    if db_connection:
        sql_file_path = os.path.join(os.path.dirname(__file__), '../sql/example_data.sql')

        seed_database_from_file(db_connection, sql_file_path)

        db_connection.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
