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
import os
import time
import logging
import argparse
from dotenv import load_dotenv

from config.paths import LOG_DIR

from utilities.database import db_connection, DB_NAME
from utilities.logger import config_logger, set_logger

from library.utils.event_display import print_event

from library.service.redis.client import RedisClient
from library.service.redis.operations.registry import RedisOperations

from library.service.kafka.config import TOPIC, CONSUMER_GROUP_ID
from library.service.kafka.consumer import create_consumer
from library.service.kafka.producer import create_producer

from library.consumers.system.handlers.dependencies import HandlerDependencies
from library.consumers.system.handlers_dispatcher import handle_event

# ----------------------------------------------------------------------------------
# --- Load Environment Variables ---
# Load variables from the .env file to the environment
load_dotenv()

# Setting up the genre
LOG_LEVEL = os.getenv("LOG_LEVEL")
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Setting up logging ---
# Log filepath
log_filepath = os.path.join(LOG_DIR, 'system_consumer.log')

# Configure the logger (uses console and file for log records)
config_logger(filepath=log_filepath, level=LOG_LEVEL)

# Setting up the logger
logger = set_logger('SYSTEM_CONSUMER')

# Silencing 'redis' logging to level 'WARNING'
logging.getLogger("redis").setLevel(logging.WARNING)
logging.getLogger("redis.connection").setLevel(logging.WARNING)
logging.getLogger("redis.client").setLevel(logging.WARNING)

# Silencing 'kafka' logging to level 'WARNING'
logging.getLogger("kafka").setLevel(logging.WARNING)
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Setting up command line argument parser ---

# Setting up argument parser via the command line
parser = argparse.ArgumentParser()

# Add `display-events` flag for displaying full event envelope in console
parser.add_argument(
    "--display-events",
    action="store_true",
    help="Display Kafka events during simulation"
)

# Parse command line arguments
args = parser.parse_args()
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Setting up consumer's handlers' dependencies ---

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
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Setting up current consumer ---
consumer = create_consumer(
    topic=TOPIC,
    consumer_name='library-system-consumer',
    group_id=CONSUMER_GROUP_ID
)
# ----------------------------------------------------------------------------------

# For each message/event in the topic
# the system fetches the event message
# and loads data in the database
for msg in consumer:

    # Save the event's message
    event = msg.value

    # Save current time for consumer performance benchmarking
    start_time = time.perf_counter()

    # Log received event in real time (NOT simulated)
    logger.info(
        f'EVENT_RECEIVED '
        f'event_type={event['event_type']} '
        f'event_id={event['event_id']} '
        f'topic={msg.topic} '
        f'partition={msg.partition} '
        f'offset={msg.offset} '
        f'group_id={CONSUMER_GROUP_ID} '
    )

    try:

        # Display event
        if args.display_events:
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

        # Log processed event in real time (NOT simulated)
        logger.info(
            f'EVENT_PROCESSED '
            f'event_type={event['event_type']} '
            f'event_id={event['event_id']} '
            f'topic={msg.topic} '
            f'partition={msg.partition} '
            f'offset={msg.offset} '
            f'group_id={CONSUMER_GROUP_ID} '
            f'duration_ms={(time.perf_counter() - start_time) * 1000:.2f}'
        )

    except Exception as e:

        # Display event
        if args.display_events:
            print_event(
                source='SYSTEM_CONSUMER_PROCESSING_ERROR',
                event=event,
            )

        # Log processing error for event in real time (NOT simulated)
        logger.error(
            f'EVENT_PROCESSING_FAILED '
            f'event_type={event['event_type']} '
            f'event_id={event['event_id']} '
            f'error_type={e.__class__.__name__}'
        )
