"""
Contains main function for retrieving records associated with a given key using a structured query
"""

import os
import psycopg2
from psycopg2.sql import SQL

from config import ROOT_DIR
from utilities.database import get_column_names

def load_query(module: str, filename: str) -> str:
    """
    Load a SQL query from the repository SQL directory

    This function reads a `.sql` file from the structured SQL folder
    api/repository/sql/<router>/<filename>.sql and returns its raw
    SQL content as a string

    :param module: str, the module name (e.g. "authors", "works", "editions")
                        used to locate the correct SQL subfolder
    :param filename: str, name of the SQL file to load

    :returns: str, the raw SQL query string read from the file
    """

    # Build absolute path to SQL file inside repository structure
    filepath = os.path.join(ROOT_DIR, 'api', 'repository', 'sql', module, filename)

    # Read SQL file
    with open(filepath, encoding='utf-8', mode='r') as f:
        query = f.read()

    return query

def execute_query(
        connection: psycopg2.extensions.connection,
        params: dict,
        query_module: str,
        query_filename: str
) -> tuple:
    """
    Retrieve all records associated with a given key using a structured query

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param filter_key: str, unique identifier of the record to retrieve
    :param query_module: str, module name where the SQL query file is located
    :param query_filename: str, name of the SQL file to load and execute.

    :returns: A tuple containing:

        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """
    # --- Read Query ---
    query = load_query(module=query_module, filename=query_filename)

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