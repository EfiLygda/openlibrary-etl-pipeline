"""

Run: python -m library.consumer.consumer.py
"""

from utilities.database import db_connection, DB_NAME

from library.core.validation import reject_event

from library.service.redis.client import RedisClient
from library.service.redis.operations.registry import RedisOperations

from library.service.kafka.config import TOPIC, CONSUMER_GROUP_ID
from library.service.kafka.consumer import create_consumer
from library.service.kafka.producer import create_producer

from library.consumer.handlers.dependencies import HandlerDependencies
from library.consumer.handlers_dispatcher import handle_event

# Establish database connection
connection = db_connection(database=DB_NAME)

# Redis client for storing ids and counters
redis_client = RedisClient()

# Producer used for emitting chain events
chain_event_producer = create_producer()

# Setting up handlers' context
handler_dependencies = HandlerDependencies(
    connection=connection,
    redis_operations=RedisOperations(redis_client),
    producer=chain_event_producer
)

# Setting up consumer of events
consumer = create_consumer(
    topic=TOPIC,
    group_id=CONSUMER_GROUP_ID
)

# For each message/event in the topic
# the consumer fetches the event message
# and loads data in the database
for msg in consumer:

    # Save the event's message
    event = msg.value

    # Reject the event, if needed, else display it
    if reject_event(redis_client, event):
        continue
    else:
        # Display event
        print(event)

    # TODO: add bulk loading of db at end of day
    # If current event type can be handled then use the proper
    # handler and load data to database
    handle_event(
        dependencies=handler_dependencies,
        event=event,
    )
