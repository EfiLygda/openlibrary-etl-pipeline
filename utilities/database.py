"""
PostgreSQL database connection utilities.

Handles environment-based configuration loading and provides
a helper function for establishing database connections using psycopg2.
"""

import os
import psycopg2
from psycopg2.sql import SQL
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

def get_column_names(cursor: psycopg2.extensions.cursor) -> list:
    """
    Fetches the column names of the last query used by the cursor

    :param cursor: psycopg2.extensions.cursor, the cursor to be used
    :return: list, list of string names or empty list if no records were available
    """

    return [d[0] for d in cursor.description] if cursor.description else []

def execute_query(
        connection: psycopg2.extensions.connection,
        query: str | None = None,
        query_filepath: str | None = None,
        params: dict | None = None,
) -> tuple:
    """
    Helper function for executing queries via a connection

    :param connection: psycopg2.extensions.connection, the connection object
    :param query: str | None, the SQL query used
    :param query_filepath: str | None, the path of the file with the SQL query
        (either 'query' or 'query_filepath' should be used, if both are given then
         only 'query' is used)
    :param params: dict | None, dictionary with the parameters to be used in the query

    :return: A tuple containing:

        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # If a query filepath is given then the SQL file is read
    # and used as the query
    if query_filepath:
        # Read SQL file
        with open(query_filepath, encoding='utf-8', mode='r') as f:
            query = f.read()

    # --- Query the database ---
    with connection.cursor() as cursor:

        # Construct the query
        query_to_execute = SQL(query)

        # Execute the query
        cursor.execute(
            query=query_to_execute,
            vars=params
        )

        # Fetch all records as returned
        data = cursor.fetchall()

        # Fetch column names as returned
        data_column_names = get_column_names(cursor)

    return data, data_column_names