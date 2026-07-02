"""
Contains simple Redis wrapper used for counters and sets in the library system
"""

import redis
from typing import Awaitable
from library.service.redis.config import REDIS_HOST, REDIS_PORT

class RedisClient:
    """
    Simple Redis wrapper used for counters and sets in the library system

    This class encapsulates Redis operations and centralizes key naming conventions:
    - Counters are stored under: count:<entity>
    - Sets are stored under: set:<entity>
    """

    def __init__(self):
        self.redis = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=0,
            decode_responses=True  # Returns strings instead of bytes
        )

    def flush_database(self) -> None:
        """
        Delete all keys in the current Redis database
        """
        self.redis.flushdb()

    def increment_counter(self, entity: str) -> int | Awaitable[int]:
        """
        Increment a Redis counter for the given entity

        :param entity: str, name of the counter (e.g. `users`, `librarians`)
        :return: int, the updated counter value
        """

        return self.redis.incr(f'count:{entity}')

    def get_counter(self, entity: str) -> int:
        """
        Get the value of a Redis counter

        :param entity: str, name of the counter
        :return: int, counter value (0 if missing)
        """

        return int(self.redis.get(f'count:{entity}') or 0)

    def add_to_set(self, entity: str, value: str | int):
        """
        Add a value to a Redis set

        :param entity: str, name of the set
        :param value: str | int, value to add to the set
        :return: int, number of elements added (0 or 1)
        """

        return self.redis.sadd(f'set:{entity}', value)

    def get_set(self, entity: str) -> set:
        """
        Retrieve all members of a Redis set

        :param entity: str, name of the set used
        :return: set[str], Set of stored values
        """

        return self.redis.smembers(f'set:{entity}')
