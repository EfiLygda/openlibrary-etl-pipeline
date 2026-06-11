"""
PostgreSQL database connection utilities.

Handles environment-based configuration loading and provides
a helper function for establishing database connections using psycopg2.
"""

import os
import psycopg2
from dotenv import load_dotenv
from typing import Generator

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
    :param autocommit: bool, whether to be able to autocommit via the connection
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

def database_dependency() -> Generator[psycopg2.extensions.connection, None, None]:
    """
    FastAPI dependency that provides a PostgreSQL database connection per request.

    :return: generator, `yields` psycopg2.extensions.connection (active DB connection),
                        `sent` into the generator None, generator `returns` when finished when
    """

    # Set up connection object
    connection = None

    # Try to make the connection with the database and return it as a generator
    # Source: https://fastapi.tiangolo.com/tutorial/sql-databases/#create-a-session-dependency
    try:

        # Make the connectio and return it as a generator
        connection = db_connection(database=DB_NAME)
        yield connection

    finally:

        # If the connection was made is not used anymore then close it
        if connection:
            connection.close()