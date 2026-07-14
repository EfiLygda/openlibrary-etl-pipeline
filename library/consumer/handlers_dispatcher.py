"""
Module responsible for dispatching events to their corresponding handlers
"""

import psycopg2

from kafka import KafkaProducer

from library.service.redis.client import RedisClient
from library.core.registry import EVENTS

def handle_event(
        connection: psycopg2.extensions.connection,
        redis_client: RedisClient,
        event: dict,
        producer: KafkaProducer,
) -> tuple:
    """
    Function for handling all events regardless of type, by inserting new records

    :param connection: psycopg2.extensions.connection, the connection used for inserting the new record
    :param redis_client: RedisClient, the redis client used to fetch configuration values
    :param event: dict, the event/dictionary used
    :param producer: KafkaProducer, producer used for emitting chain events, when needed

    :return: tuple, the tuple containing:
        * `data` - list of matching records returned by the query
        * `data_column_names` - column names corresponding to the records
    """

    # Save event type
    event_type = event['event_type']

    # Fetch event spec
    event_spec = EVENTS[event_type]

    # Get the current event's counter name and its key (if the counter is in a hash)
    # for Redis
    counter_name = event_spec.counter_name
    counter_hash_key = event_spec.get_counter_hash_key(event)

    # Increment event counter
    counter = redis_client.counters.increment_counter(
        name=counter_name,
        key=counter_hash_key
    )

    if event_spec.produces_event:
        return event_spec.handler(
            connection=connection,
            redis_client=redis_client,
            event=event,
            counter=counter,
            producer=producer
        )

    return event_spec.handler(
        connection=connection,
        redis_client=redis_client,
        event=event,
        counter=counter
    )
