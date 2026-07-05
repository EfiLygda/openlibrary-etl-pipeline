"""
Module with the library's event handlers
"""

import os
import psycopg2

from config.paths import LIBRARY_ROOT
from utilities import execute_query

from library.service.redis.service import RedisClient

# Path for SQL commands used for generating data
SQL_DIR = os.path.join(LIBRARY_ROOT, 'consumer', 'sql')

def handle_librarian_hired(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int
) -> tuple:
    """
    Inserts new hired librarian record to the 'librarians' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """
    
    # Generate new librarian ID
    new_librarian_id = f'LB-{counter}'

    # Add new ID to Redis set to be used later
    redis_client.add_to_set('librarians:ids', new_librarian_id)

    # Setting up the loading query
    query_filepath = os.path.join(SQL_DIR, 'insert_librarian.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'librarian_id': new_librarian_id,
            'first_name': event['data']['first_name'],
            'last_name': event['data']['last_name'],
            'email': event['data']['email'],
            'registered_at': event['timestamp'],
        }
    )

def handle_user_registered(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int
) -> tuple:
    """
    Inserts new registered user record to the 'users' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Generate new user ID
    new_user_id = f'USR-{counter}'

    # Add new ID to Redis set to be used later
    redis_client.add_to_set('users:ids', new_user_id)

    # Setting up the loading query
    query_filepath = os.path.join(SQL_DIR, 'insert_user.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'user_id': new_user_id,
            'first_name': event['data']['first_name'],
            'last_name': event['data']['last_name'],
            'email': event['data']['email'],
            'registered_at': event['timestamp'],
        }
    )

def handle_copy_purchased(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int
) -> tuple:
    """
    Inserts new purchased copy record to the 'copies' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Generate new copy ID
    new_copy_id = f'{event['data']['edition_key']}-{counter}'

    # Add new ID to Redis set to be used later
    redis_client.add_to_set('copies:available:ids', new_copy_id)

    # Setting up the loading query
    query_filepath = os.path.join(SQL_DIR, 'insert_copy.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'copy_id': new_copy_id,
            'edition_key': event['data']['edition_key'],
            'status': 'AVAILABLE',
            'registered_at': event['timestamp'],
        }
    )

def handle_copy_borrowed(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int
) -> tuple:
    """
    Inserts new record of a copy's borrowing to the 'loans' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Generate new copy ID
    new_loan_id = f'LN-{counter}'

    # Add new ID to Redis set to be used later
    redis_client.add_to_set('loans:active:ids', new_loan_id)

    # Move copy id from available to unavailable in Redis
    redis_client.move_sets(
        source='copies:available:ids',
        destination='copies:unavailable:ids',
        value=event['data']['copy_id']
    )

    # Setting up the loading query
    query_filepath = os.path.join(SQL_DIR, 'insert_loan_update_copies.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'loan_id': new_loan_id,
            'user_id': event['data']['user_id'],
            'copy_id': event['data']['copy_id'],

            'borrow_date': event['timestamp'],
            'due_date': event['data']['due_date'],
            'return_date': None,

            'renewal_count': 0,
            'status': 'ACTIVE', # "ACTIVE | RETURNED"
            'processed_by':  event['data']['librarian_id']
        }
    )

HANDLERS = {
    'LIBRARIAN_HIRED': handle_librarian_hired,
    'USER_REGISTERED': handle_user_registered,
    'COPY_PURCHASED': handle_copy_purchased,
    'BORROW': handle_copy_borrowed,

    # 'RETURN': handle_return,
    # 'RESERVE': handle_reserve,
}

def handle_event(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int
) -> tuple:
    """
    Function for handling all events regardless of type, by inserting new records

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    return HANDLERS[event['event_type']](
        connection=connection,
        redis_client=redis_client,
        event=event,
        counter=counter
    )