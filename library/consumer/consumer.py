"""

Run: python -m library.consumer.consumer.py
"""

import json

from kafka import KafkaConsumer

from utilities.database import db_connection, DB_NAME

from library.core.registry import EVENTS
from library.core.validation import reject_event

from library.service.redis.service import RedisClient
from library.service.kafka.config import TOPIC, BOOTSTRAP, CONSUMER_GROUP_ID, AUTO_OFFSET_RESET

from library.consumer.handlers_dispatcher import handle_event

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

    # Reject the event, if needed, else display it
    if reject_event(redis_client, event):
        continue
    else:
        # Display event
        print(event)

    # Save event type
    event_type = event['event_type']

    # Fetch event spec
    event_spec = EVENTS[event_type]

    # Get the current event's counter for Redis
    counter_name = event_spec.counter_name(event)

    # Increment event counter
    counter = redis_client.increment_counter(counter_name)

    # TODO: add bulk loading of db at end of day
    # If current event type can be handled then use the proper
    # handler and load data to database
    data, _ = handle_event(
        connection=connection,
        redis_client=redis_client,
        event=event,
        counter=counter
    )
