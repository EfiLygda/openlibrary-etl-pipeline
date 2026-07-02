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
    - Counters are stored under: count:<name>
    - Sets are stored under: set:<name>
    - Hashes are stored under: hash:<name>
    """

    def __init__(self, database: int = 0):
        self.redis = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=database,
            decode_responses=True  # Returns strings instead of bytes
        )

    def flush_database(self) -> None:
        """
        Delete all keys in the current Redis database
        """
        self.redis.flushdb()

    def increment_counter(self, name: str) -> int | Awaitable[int]:
        """
        Increment a Redis counter for the given name

        :param name: str, name of the counter (e.g. `users`, `librarians`, `edition:OL123M`)
        :return: int, the updated counter value
        """

        return self.redis.incr(f'count:{name}')

    def get_counter(self, name: str) -> int:
        """
        Get the value of a Redis counter

        :param name: str, name of the counter (e.g. `users`, `librarians`, `edition:OL123M`)
        :return: int, counter value (0 if missing)
        """

        return int(self.redis.get(f'count:{name}') or 0)

    def add_to_set(self, name: str, *values):
        """
        Add a value to a Redis set

        :param name: str, name of the set (e.g. `users`, `librarians`)
        :param values: values to add to the set
        :return: int, number of elements added (0 or 1)
        """

        return self.redis.sadd(f'set:{name}', *values)

    def get_set(self, name: str) -> set:
        """
        Retrieve all members of a Redis set

        :param name: str, name of the set used
        :return: set[str], Set of stored values
        """

        return self.redis.smembers(f'set:{name}')

    def get_random_from_set(self, name: str) -> bytes | str | list[bytes | str] | None:
        """
        Retrieve a random member from a Redis set

        :param name: str, name of the set used
        :return: str, the random value
        """

        return self.redis.srandmember(f'set:{name}')

    def add_hash(self, name: str, mapping: dict) -> int:
        """
        Set a dictionary as a hash Redis in one go

        :param name: str, name of the hash used
        :param mapping: dict, the dictionary used

        :return: int, the number of fields that were added
        """

        return self.redis.hset(f'hash:{name}', mapping=mapping)

    def get_from_hash(self, name: str, key: str) -> bytes | str | None:
        """
        Retrieve the value of key from a Redis hash

        :param name: str, name of the hash used
        :param key: str, key of the value to retrieve

        :return: bytes | str | None, the wanted value
        """

        return self.redis.hget(f'hash:{name}', key=key)
