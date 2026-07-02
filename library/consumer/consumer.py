"""

Run: python -m library.consumer.consumer.py
"""

import json

from kafka import KafkaConsumer

from library.service.redis.service import RedisClient
from utilities.database import db_connection, DB_NAME

from library.service.kafka.config import TOPIC, BOOTSTRAP, CONSUMER_GROUP_ID, AUTO_OFFSET_RESET
from library.consumer.handlers import HANDLERS

# Establish database connection
connection = db_connection(database=DB_NAME)

# Redis client for storing ids and counters
redis_client = RedisClient()

# Setting up consumer of events
consumer = KafkaConsumer(
    TOPIC,
    bootstrap_servers=BOOTSTRAP,
    value_deserializer=lambda v: json.loads(v.decode("utf-8")),
    auto_offset_reset=AUTO_OFFSET_RESET,
    group_id=CONSUMER_GROUP_ID
)

# For each message/event in the topic
# the consumer fetches the event message
# and loads data in the database
for msg in consumer:

    # Save the event's message
    event = msg.value

    # Print basic event metadata
    print("EVENT RECEIVED:")
    print(event["event_type"], event["data"], event['timestamp'])

    # Save event type
    event_type = event['event_type']

    # TODO: add bulk loading of db at end of day
    if event_type in HANDLERS.keys():
        HANDLERS[event_type](connection=connection, event=event)
