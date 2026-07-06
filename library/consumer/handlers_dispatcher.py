"""
Module responsible for dispatching events to their corresponding handlers
"""

import psycopg2
from library.service.redis.service import RedisClient

from library.consumer.handlers import people
from library.consumer.handlers import inventory
from library.consumer.handlers import circulation

# Dictionary for dispatching handlers
HANDLERS = {
    'LIBRARIAN_HIRED': people.handle_librarian_hired,
    'USER_REGISTERED': people.handle_user_registered,
    'COPY_PURCHASED': inventory.handle_copy_purchased,
    'BORROW': circulation.handle_copy_borrowed,
    'RETURN': circulation.handle_return_borrowed_copy,

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