"""

Run: python -m library.producer.producer.py
"""

import json
from random import random, seed, uniform
from datetime import datetime

from kafka import KafkaProducer

from utilities.rate_limit import wait
from utilities.database import db_connection, DB_NAME

from library.kafka_config import BOOTSTRAP, TOPIC
from library.producer.producer_config import SEED, END_DATE, MAX_USERS, MAX_LIBRARIANS, COPIES
from library.producer.event_generator import generate_event

# Seeding random module
seed(SEED)

# Establish connection with the database
connection = db_connection(database=DB_NAME)

# Setting up the Kafka producer
producer = KafkaProducer(
    bootstrap_servers=BOOTSTRAP,
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

# Event counters used for validation
event_counters = {
    'USER_REGISTERED': 0,
    'COPY_PURCHASED': {
        k: 0 for k in COPIES.keys()
    },
    'BORROW': 0,
    'RETURN': 0,
    'RESERVE': 0,
    'LIBRARIAN_HIRED': 0
}

# The maximum amounts of events that will be allowed
max_event_values = {
    'USER_REGISTERED': MAX_USERS,
    'COPY_PURCHASED': COPIES,
    'BORROW': 0,
    'RETURN': 0,
    'RESERVE': 0,
    'LIBRARIAN_HIRED': MAX_LIBRARIANS
}

# Starting producer simulation
while True:

    # Generate an event
    event = generate_event(connection=connection)

    # If the event's timestamp is over the end date
    # then the simulation stops
    if datetime.fromisoformat(event['timestamp']) >= END_DATE:
        break

    # Save current event's type
    event_type = event['event_type']

    # Counting events and validating if they should be used
    # Mainly if their number is over the predetermined max
    if event_type == 'COPY_PURCHASED':
        copy_edition = event['data']['edition_key']
        max_value = max_event_values['COPY_PURCHASED'][copy_edition]
        counter = event_counters['COPY_PURCHASED'][copy_edition]

        if counter <= max_value:
            event_counters['COPY_PURCHASED'][copy_edition] += 1
        else:
            continue

    else:
        max_value = max_event_values[event_type]
        counter = event_counters[event_type]

        if counter <= max_value:
            event_counters[event_type] += 1
        else:
            continue

    # Display event
    print(event)

    # Publish the event to chosen topic
    producer.send(TOPIC, value=event)

    # All buffered events are immidietly available
    # TODO: add batches
    producer.flush()

    # Wait before next event with jitter
    jitter = uniform(-0.1, 0.1)
    wait(max(0, 0.5 + jitter))
