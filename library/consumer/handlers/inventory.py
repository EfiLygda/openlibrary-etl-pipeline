"""
Event handlers related to library inventory.

Handles events involving physical copies of works, such as:
* Copy purchases
"""

from library.consumer.handlers.paths import INVENTORY_SQL_DIR
from library.consumer.handlers.dependencies import HandlerDependencies
from library.database.handler_queries import execute_handler_query

def handle_copy_purchased(
        dependencies: HandlerDependencies,
        counter: int,
        event: dict,
) -> None:
    """
    Inserts new purchased copy record to the 'copies' table

    :param dependencies: HandlerDependencies, contains shared resources required
        by the handler, such as the database connection, Redis operations,
        and event producer
    :param counter: int, the event counter used for generating a record's ID
    :param event: dict, the event/dictionary used

    :return: None
    """

    # Generate new copy ID
    new_copy_id = f'{event['payload']['edition_key']}-{counter}'

    # Add new ID to Redis set to be used later
    dependencies.redis_operations.copies.register_copy(
        copy_id=new_copy_id
    )

    # Execute the query
    execute_handler_query(
        connection=dependencies.connection,
        event_category_dir=INVENTORY_SQL_DIR,
        sql_filename='copy_purchased.sql',
        params={
            'copy_id': new_copy_id,
            'edition_key': event['payload']['edition_key'],
            'status': 'AVAILABLE',
            'registered_at': event['timestamp'],
        }
    )
