"""

Run: python -m library.producer.producer.py
"""

from random import seed, uniform
from datetime import datetime

from utilities.rate_limit import wait

from library.core.validation import reject_event

from library.service.kafka.config import TOPIC
from library.service.kafka.producer import create_producer
from library.service.redis.service import RedisClient

from library.producer.producer_config import SEED, END_DATE
from library.service.kafka.publisher import emit_event
from library.producer.simulation.event_generator import generate_event

# Seeding random module
seed(SEED)

# Setting up redis for live state
redis_client = RedisClient()

# Setting up the Kafka producer
producer = create_producer()

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
        continue

    # Display allowed event
    print(event)

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
redis_client.flush_database()

# Close the client
redis_client.close()
