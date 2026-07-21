"""
Main entry point for the library event producer simulation.

This script continuously generates simulated library events, validates them
against the current system state stored in Redis, and publishes accepted
events to Kafka. The simulation runs until an event reaches the configured
end date.

Note:
    Redis is not a cache. It is the current world state that determines whether
    an event is even possible.

Workflow:
    1. Seed the random number generator for reproducible simulations.
    2. Initialize Redis and the Kafka producer.
    3. Generate candidate events.
    4. Reject invalid events based on business rules.
    5. Publish valid events to Kafka.
    6. Wait for a short randomized interval before generating the next event.
    7. Clean up Redis and close connections when the simulation ends.

Run:
    python -m library.producer.producer.py
"""
import argparse
import os
from dotenv import load_dotenv
import logging

from random import seed, uniform
from datetime import datetime

from config.paths import LOG_DIR
from utilities.logger import config_logger, set_logger
from utilities.rate_limit import wait

from library.core.validation import reject_event
from library.utils.event_display import print_event

from library.service.kafka.config import TOPIC
from library.service.kafka.producer import create_producer
from library.service.redis.client import RedisClient

from library.producer.producer_config import SEED, END_DATE
from library.service.kafka.publisher import emit_event
from library.producer.simulation.event_generator import generate_event

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
# Seeding random module
seed(SEED)
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# Setting up redis for live state
redis_client = RedisClient()

# Setting up the Kafka producer
producer = create_producer()
# ----------------------------------------------------------------------------------

# Starting producer simulation
while True:

    # Generate an event
    event = generate_event(redis_client=redis_client)

    # If the event's timestamp is over the end date of the simulation
    # then the simulation stops
    if datetime.fromisoformat(event['timestamp']) >= END_DATE:
        break

    # Reject event if needed
    if reject_event(redis_client, event):

        if args.display_events:
            # Display rejected event
            print_event(
                source='REJECTED',
                event=event,
            )

        continue

    if args.display_events:
        # Display allowed event
        print_event(
            source='PRODUCER',
            event=event,
        )

    # Publish the allowed event to chosen topic
    emit_event(
        producer=producer,
        topic=TOPIC,
        event=event
    )

    # Wait before next event with jitter
    jitter = uniform(-0.1, 0.1)
    wait(max(0, 0.5 + jitter))

# Delete everything from Redis database after the end of the simulation
redis_client.database.flush()

# Close the client
redis_client.close()
