"""
Utility functions for executing SQL queries triggered by event handlers
"""

import os
import psycopg2
from utilities.database import execute_query


def execute_handler_query(
    connection: psycopg2.extensions.connection,
    event_category_dir: str,
    sql_filename: str,
    params: dict,
) -> None:
    """
    Executes an SQL query associated with an event handler.

    Builds the query file path using the provided event category directory and
    SQL filename, then executes the query with the provided parameters.

    :param connection: psycopg2.extensions.connection, the database connection used for executing the query
    :param event_category_dir: str, the directory containing SQL files for the event category
    :param sql_filename: str, the name of the SQL file to execute
    :param params: dict, the parameters passed to the SQL query

    :return: None
    """

    # Setting up the query
    query_filepath = os.path.join(
        event_category_dir,
        sql_filename
    )

    # Execute the query
    execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params=params,
    )
