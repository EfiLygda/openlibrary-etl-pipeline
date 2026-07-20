"""
Main entry point for the library event processing system.

This script consumes library events from Kafka, validates them against the
current system state, and dispatches accepted events to their corresponding
handlers. Event handlers update the relational database, maintain Redis state,
and may emit additional chain events back to Kafka.

Note:
    Redis is not a cache. It is the current world state that determines whether
    an event is even possible.

Workflow:
    1. Establish a database connection.
    2. Initialize Redis and the Kafka producer used for chain events.
    3. Create the handler dependency context.
    4. Subscribe to the configured Kafka topic.
    5. Consume events continuously.
    6. Reject invalid events based on business rules.
    7. Dispatch valid events to the appropriate handler.

Run:
    python -m library.consumers.system.consumer.py
"""

from utilities.database import db_connection, DB_NAME

from library.core.validation import reject_event
from library.utils.event_display import print_event

from library.service.redis.client import RedisClient
from library.service.redis.operations.registry import RedisOperations

from library.service.kafka.config import TOPIC, CONSUMER_GROUP_ID
from library.service.kafka.consumer import create_consumer
from library.service.kafka.producer import create_producer

from library.consumers.system.handlers.dependencies import HandlerDependencies
from library.consumers.system.handlers_dispatcher import handle_event

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
    chain_event_producer=chain_event_producer
)

# Setting up system of events
consumer = create_consumer(
    topic=TOPIC,
    group_id=CONSUMER_GROUP_ID
)

# For each message/event in the topic
# the system fetches the event message
# and loads data in the database
for msg in consumer:

    # Save the event's message
    event = msg.value

    # Display event
    print_event(
        source='SYSTEM_CONSUMER',
        event=event,
    )

    # TODO: add bulk loading of db at end of day
    # If current event type can be handled then use the proper
    # handler and load data to database
    handle_event(
        dependencies=handler_dependencies,
        event=event,
    )
