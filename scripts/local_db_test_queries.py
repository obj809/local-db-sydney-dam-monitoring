# scripts/local_db_test_queries.py

import os
import mysql.connector
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
        'database': os.getenv('LOCAL_DB_NAME'),
        'user': os.getenv('LOCAL_DB_USER'),
        'password': os.getenv('LOCAL_DB_PASSWORD'),
    }

    # Validate that required configurations are present
    missing = [key for key, value in db_config.items() if value is None]
    if missing:
        print(f"Error: Missing environment variables: {', '.join(missing)}")
        exit(1)

    return db_config


def connect_to_database(db_config):
    """Establish a connection to the local MySQL database."""
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
    """
    Execute SQL queries from a file and print the results.

    Args:
        connection (mysql.connector.connection.MySQLConnection): The database connection.
        sql_file_path (str): The path to the SQL file containing queries.
    """
    cursor = connection.cursor(dictionary=True)  # Use dictionary=True to get results as dict
    try:
        # Open and read the SQL file
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()

        # Split the SQL script into individual queries
        sql_queries = sql_script.split(';')

        # Execute each query and print results
        for index, query in enumerate(sql_queries):
            if query.strip():  # Skip empty or whitespace-only queries
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
    """Main execution block to execute SQL queries."""
    # Load environment variables
    load_environment_variables()

    # Get database configuration
    db_config = get_db_config()

    # Connect to the database
    db_connection = connect_to_database(db_config)

    if db_connection:
        # Define the path to the SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), '../sql/example_queries.sql')

        # Execute queries and print the results
        execute_queries(db_connection, sql_file_path)

        # Close the connection
        db_connection.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
