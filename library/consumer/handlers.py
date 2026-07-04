"""
Module with the library's event handlers
"""

import os
import psycopg2

from config.paths import LIBRARY_ROOT
from utilities import execute_query

# Path for SQL commands used for generating data
SQL_DIR = os.path.join(LIBRARY_ROOT, 'consumer', 'sql')

def handle_librarian_hired(
        connection: psycopg2.extensions.connection,
        event: dict
) -> tuple:
    """
    Inserts new hired librarian record to the 'librarians' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param event: dict, the event/dictionary used

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Setting up the loading query
    query_filepath = os.path.join(SQL_DIR, 'insert_librarian.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'first_name': event['data']['first_name'],
            'last_name': event['data']['last_name'],
            'email': event['data']['email'],
            'registered_at': event['timestamp'],
        }
    )

def handle_user_registered(
        connection: psycopg2.extensions.connection ,
        event: dict
) -> tuple:
    """
    Inserts new registered user record to the 'users' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param event: dict, the event/dictionary used

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Setting up the loading query
    query_filepath = os.path.join(SQL_DIR, 'insert_user.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'first_name': event['data']['first_name'],
            'last_name': event['data']['last_name'],
            'email': event['data']['email'],
            'registered_at': event['timestamp'],
        }
    )

def handle_copy_purchased(
        connection: psycopg2.extensions.connection ,
        event: dict
) -> tuple:
    """
    Inserts new purchased copy record to the 'copies' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param event: dict, the event/dictionary used

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Setting up the loading query
    query_filepath = os.path.join(SQL_DIR, 'insert_copy.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'edition_key': event['data']['edition_key'],
            'status': 'AVAILABLE',
            'registered_at': event['timestamp'],
        }
    )

HANDLERS = {
    'LIBRARIAN_HIRED': handle_librarian_hired,
    'USER_REGISTERED': handle_user_registered,
    'COPY_PURCHASED': handle_copy_purchased,

    # 'BORROW': handle_borrow,
    # 'RETURN': handle_return,
    # 'RESERVE': handle_reserve,
}

def handle_event(
        connection: psycopg2.extensions.connection,
        event: dict
) -> tuple:
    """
    Function for handling all events regardless of type, by inserting new records

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param event: dict, the event/dictionary used

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    return HANDLERS[event['event_type']](
        connection=connection,
        event=event
    )