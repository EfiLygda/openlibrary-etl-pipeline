"""
Event handlers related to library inventory.

Handles events involving physical copies of works, such as:
* Copy purchases
"""

import psycopg2
from kafka import KafkaProducer

from library.consumer.handlers.paths import INVENTORY_SQL_DIR
from library.database.handler_queries import execute_handler_query
from library.service.redis.operations.registry import RedisOperations

def handle_copy_purchased(
        connection: psycopg2.extensions.connection,
        redis_operations: RedisOperations,
        event: dict,
        counter: int,
        producer: KafkaProducer | None = None,
) -> None:
    """
    Inserts new purchased copy record to the 'copies' table

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_operations: RedisOperations, the Redis operations handler
    :param event: dict, the event/dictionary used
    :param counter: int, the event counter used for generating a record's ID
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: None
    """

    # Generate new copy ID
    new_copy_id = f'{event['data']['edition_key']}-{counter}'

    # Add new ID to Redis set to be used later
    redis_operations.copies.register_copy(
        copy_id=new_copy_id
    )

    # Execute the query
    execute_handler_query(
        connection=connection,
        event_category_dir=INVENTORY_SQL_DIR,
        sql_filename='copy_purchased.sql',
        params={
            'copy_id': new_copy_id,
            'edition_key': event['data']['edition_key'],
            'status': 'AVAILABLE',
            'registered_at': event['timestamp'],
        }
    )
