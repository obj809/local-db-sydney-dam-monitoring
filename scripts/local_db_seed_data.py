# scripts/local_db_seed_data.py

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


def seed_database_from_file(connection, sql_file_path):
    """
    Seed the database using an SQL file.

    Args:
        connection (mysql.connector.connection.MySQLConnection): The database connection.
        sql_file_path (str): The path to the SQL file containing seed data.
    """
    cursor = connection.cursor()
    try:
        # Open and read the SQL file
        with open(sql_file_path, 'r') as file:
            sql_script = file.read()

        # Split the SQL script into individual statements
        sql_commands = sql_script.split(';')
        for command in sql_commands:
            # Skip empty or whitespace-only commands
            if command.strip():
                cursor.execute(command)
        
        # Commit the changes to the database
        connection.commit()
        print(f"Data from {sql_file_path} has been seeded into the database successfully!")

    except FileNotFoundError:
        print(f"Error: The file {sql_file_path} does not exist.")
    except mysql.connector.Error as err:
        print(f"Error while seeding data: {err}")
    finally:
        cursor.close()


def main():
    """Main execution block to seed the local database."""
    # Load environment variables
    load_environment_variables()

    # Get database configuration
    db_config = get_db_config()

    # Connect to the database
    db_connection = connect_to_database(db_config)

    if db_connection:
        # Define the path to the SQL file
        sql_file_path = os.path.join(os.path.dirname(__file__), '../sql/example_data.sql')

        # Seed the database using the SQL file
        seed_database_from_file(db_connection, sql_file_path)

        # Close the connection
        db_connection.close()
        print("Database connection closed.")


if __name__ == "__main__":
    main()
