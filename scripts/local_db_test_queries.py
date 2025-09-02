# scripts/local_db_test_queries.py

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


def execute_queries(connection, sql_file_path):

    cursor = connection.cursor(dictionary=True)
    try:
        
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()

        sql_queries = sql_script.split(';')

        for index, query in enumerate(sql_queries):
            if query.strip():
                print(f"\nExecuting Query {index + 1}:\n{query.strip()}")
                cursor.execute(query)
                results = cursor.fetchall()

                print(f"Results for Query {index + 1}:")
                if results:
                    for row in results:
                        print(row)
                else:
                    print("No results found.")

    except FileNotFoundError:
        print(f"Error: The file {sql_file_path} does not exist.")
    except mysql.connector.Error as err:
        print(f"Error while executing queries: {err}")
    finally:
        cursor.close()


def main():
    
    load_environment_variables()

    db_config = get_db_config()

    db_connection = connect_to_database(db_config)

    if db_connection:
        sql_file_path = os.path.join(os.path.dirname(__file__), '../sql/example_queries.sql')

        execute_queries(db_connection, sql_file_path)

        db_connection.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
