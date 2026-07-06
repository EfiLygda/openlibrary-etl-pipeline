"""
Event handlers related to library circulation.

Handles events involving lending workflows, such as:
* Borrowing copies
* Returning borrowed copies
* Renewing loans
"""

import os
import psycopg2

from config.paths import CONSUMER_SQL_DIR
from library.utils.dates import add_days_to_str_date
from utilities import execute_query

from library.service.redis.keys import RedisKeys
from library.service.redis.service import RedisClient


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
    redis_client.add_to_set(
        RedisKeys.Sets.ACTIVE_LOANS_IDS,
        new_loan_id
    )

    # Setting up loan's hash
    redis_client.add_hash(
        RedisKeys.Hashes.loan(new_loan_id),
        mapping={
            'copy_id': event['data']['copy_id'],
            'due_date': event['data']['due_date'],
            # TODO: Maybe add more
            # 'user_id': None,
        }
    )

    # Move copy id from available to unavailable in Redis
    redis_client.move_sets(
        source=RedisKeys.Sets.AVAILABLE_COPIES_IDS,
        destination=RedisKeys.Sets.UNAVAILABLE_COPIES_IDS,
        value=event['data']['copy_id']
    )

    # Setting up the loading query
    query_filepath = os.path.join(CONSUMER_SQL_DIR, 'insert_loan_update_copies.sql')

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

def handle_return_borrowed_copy(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int
) -> tuple:
    """
    Updates the loan's and the respective copy's status in the database

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Fetch the loan it from the even
    loan_id = event['data']['loan_id']

    # Fetch the copy from the loan's Redis hash
    loan_copy_id = str(
        redis_client.get_from_hash(
            name=RedisKeys.Hashes.loan(loan_id),
            key='copy_id'
        )
    )

    # Move loan ID from active loans to returned loans set
    redis_client.move_sets(
        RedisKeys.Sets.ACTIVE_LOANS_IDS,
        RedisKeys.Sets.RETURNED_LOANS_IDS,
        loan_id
    )

    # Move copy id from unavailable to available in Redis
    redis_client.move_sets(
        source=RedisKeys.Sets.UNAVAILABLE_COPIES_IDS,
        destination=RedisKeys.Sets.AVAILABLE_COPIES_IDS,
        value=loan_copy_id
    )

    # Setting up the loading query
    query_filepath = os.path.join(CONSUMER_SQL_DIR, 'return_update_loans_update_copies.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'loan_id': loan_id,
            'copy_id': loan_copy_id,
            'return_date': event['timestamp']
        }
    )

def handle_renewal_of_borrowed_copy(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        counter: int
) -> tuple:
    """
    Updates the loans due date and renewal count in 'loans' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Fetch the loan it from the even
    loan_id = event['data']['loan_id']

    # Build new due date after renewal
    new_due_date = add_days_to_str_date(
        date=str(
            redis_client.get_from_hash(
                name=RedisKeys.Hashes.loan(loan_id),
                key='due_date'
            )
        ),
        days=7
    )

    # Add new due date to loan's hash
    redis_client.set_in_hash(
        name=RedisKeys.Hashes.loan(loan_id),
        key='due_date',
        value=new_due_date
    )

    # Setting up the loading query
    query_filepath = os.path.join(CONSUMER_SQL_DIR, 'renewal_update_loans.sql')

    # Execute the query
    return execute_query(
        connection=connection,
        query_filepath=query_filepath,
        params={
            'loan_id': loan_id,
            'new_due_date': new_due_date,
        }
    )