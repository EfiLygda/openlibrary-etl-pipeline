"""
Initializes Redis for the simulation environment

This script:
- Connects to Redis via RedisClient
- Flushes the existing Redis database
- Builds the simulation context (users, librarians, editions, limits)
- Stores global simulation parameters into Redis
- Loads per-edition maximum copy limits using a Redis pipeline for efficiency

Intended to bootstrap the Redis state for the producer/consumer simulation workflow
"""
from utilities.logging import set_logger

from library.service.redis.keys import RedisKeys
from library.service.redis.client import RedisClient
from library.producer.simulation.bootstrap import build_context

logger = set_logger('INITIALIZE_SIMULATION')

def run():

    logger.info('STAGE_START')

    # Setting up redis for live state
    redis_client = RedisClient()

    # Delete everything from Redis database
    redis_client.database.flush_database()

    # Build simulation world context
    simulation_context = build_context()

    # Add simulation context to Redis
    redis_client.sets.add_to_set(
        RedisKeys.Sets.EDITION_KEYS,
        *simulation_context['edition_keys']
    )

    redis_client.strings.set_value(
        RedisKeys.Strings.MAX_USERS,
        simulation_context['max_users']
    )

    redis_client.strings.set_value(
        RedisKeys.Strings.MAX_LIBRARIANS,
        simulation_context['max_librarians']
    )

    redis_client.hashes.add_hash(
        name=RedisKeys.Hashes.MAX_EDITION_COPIES,
        mapping=simulation_context['max_copies_per_edition']
    )

    # Close the client
    redis_client.close()

    logger.info('STAGE_COMPLETE')

