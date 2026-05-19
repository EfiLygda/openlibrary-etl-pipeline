import os
import psycopg2
from dotenv import load_dotenv

# --- Load Environment Variables ---
# Load variables from the .env file to the environment
load_dotenv()

# Save the hidden info to variables
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

def db_connection(
        database: str = '',
        autocommit: bool = True
) -> psycopg2.extensions.connection:
    """
    Function for establishing a PostgreSQL server connection
    :param database:
    :param autocommit: bool, whether or not to be able to autocommit via the connection
    :return: psycopg2.extensions.connection, the connection object
    """

    # Establish a connection to the PostgreSQL server
    if database:
        connection = psycopg2.connect(
            database=database,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
    else:
        connection = psycopg2.connect(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )

    # Use autocommit in order to be able to create tables inside a transaction block
    connection.autocommit = autocommit

    return connection
