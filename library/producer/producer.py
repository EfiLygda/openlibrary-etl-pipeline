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

from random import seed, uniform
from datetime import datetime

from utilities.rate_limit import wait

from library.core.validation import reject_event
from library.utils.event_display import print_event

from library.service.kafka.config import TOPIC
from library.service.kafka.producer import create_producer
from library.service.redis.client import RedisClient

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
        # Display rejected event
        print_event(
            source='REJECTED',
            event=event,
        )

        continue

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
