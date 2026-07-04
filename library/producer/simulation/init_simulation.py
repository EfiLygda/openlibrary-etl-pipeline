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

from library.service.redis.service import RedisClient
from library.producer.simulation.bootstrap import build_context

logger = set_logger('INITIALIZE_SIMULATION')

def run():

    logger.info('STAGE_START')

    # Setting up redis for live state
    redis_client = RedisClient()

    # Delete everything from Redis database
    redis_client.flush_database()

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

    # Close the client
    redis_client.close()

    logger.info('STAGE_COMPLETE')

