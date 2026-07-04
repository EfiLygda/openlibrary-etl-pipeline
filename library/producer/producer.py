"""

Run: python -m library.producer.producer.py
"""

import json
from random import seed, uniform
from datetime import datetime

from kafka import KafkaProducer

from utilities.rate_limit import wait
from utilities.database import db_connection, DB_NAME

from library.core.validation import reject_event

from library.service.kafka.config import BOOTSTRAP, TOPIC
from library.service.redis.service import RedisClient

from library.producer.producer_config import SEED, END_DATE
from library.producer.simulation.bootstrap import build_context
from library.producer.simulation.event_generator import generate_event

# Seeding random module
seed(SEED)

# Establish connection with the database
connection = db_connection(database=DB_NAME)

# Setting up redis for live state
redis_client = RedisClient()

# Delete everything from Redis database
redis_client.flush_database()

# Setting up the Kafka producer
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# -------------------------------------------------------------
# TODO: Add this to simulation_init.py and import it here

# Build simulation world context
simulation_context = build_context()

# Add simulation context to Redis
redis_client.add_to_set('editions:keys', *simulation_context['edition_keys'])
redis_client.set_value('max:users', simulation_context['max_users'])
redis_client.set_value('max:librarians', simulation_context['max_librarians'])

# Loading all max edition copies to Redis database via pipeline
# for decreasing loading time
with redis_client.pipeline() as pipe:

    # For each edition key and its respective simulation maximum allowable number of copies
    # the pair is loaded to a Redis database in order to be used from the producer and
    # the consumer (mainly for rejecting events)
    for edition_key, max_allowable_copies in simulation_context['max_copies_per_edition'].items():

        # Set the key, value pairs via the pipeline
        pipe.set(
            name=f'max:edition:{edition_key}:copies',
            value=max_allowable_copies
        )

    # Execute whole pipeline at once
    pipe.execute()
# -------------------------------------------------------------

# Starting producer simulation
while True:

    # Generate an event
    event = generate_event(redis_client=redis_client)

    # If the event's timestamp is over the end date of the simulation
    # then the simulation stops
    if datetime.fromisoformat(event['timestamp']) >= END_DATE:
        break

    if reject_event(redis_client, event):
        continue

    # Display allowed event
    print(event)

    # Publish the allowed event to chosen topic
    producer.send(TOPIC, value=event)

    # All buffered events are immediately available
    # TODO: add batches
    producer.flush()

    # Wait before next event with jitter
    jitter = uniform(-0.1, 0.1)
    wait(max(0, 0.5 + jitter))

# Delete everything from Redis database after the end of the simulation
redis_client.flush_database()