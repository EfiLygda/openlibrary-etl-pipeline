"""
Contains simple Redis wrapper used for counters and sets in the library system

Redis naming conventions:
* Global IDs' Pools
    - editions (SET) - all edition keys available in the database
    - users (SET) - runtime user ids
    - librarians (SET) - runtime librarian ids
    - copies (SET) - runtime copy ids

* Maximum Allowable Values
    - max:users (INT) - max users to register
    - max:librarians (INT) - max librarians to hire
    - max:edition:{edition_key}:copies (INT) - max copies for current edition_key

* Runtime Counters
    - counter:users (INCR) - counting current registered users
    - counter:librarians (INCR) - counting current hired librarians
    - counter:edition:{edition_key}:copies (INCR) - counting current edition's copies purchased
"""

from typing import Awaitable

import redis
from redis.client import Pipeline

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

    @staticmethod
    def build_redis_key(*key_parts: str) -> str:
        """
        Helper method for building a Redis key

        :return: str, the redis key
        """
        return ':'.join(key_parts)

    def pipeline(self) -> Pipeline:
        """
        Redis pipeline for queuing multiple commands for later execution
        """
        return self.redis.pipeline()

    def set_value(self, name: str, value: int | str) -> bool | str | bytes | None:
        """
        Set a ``value`` to key ``name``

        :param name: str, name of the variable
        :param value: str, value of the variable

        :return: bool | str | bytes | None, whether the value was set or not
        """
        return self.redis.set(name, value)

    def get_value(self, name: str) -> bytes | str | None:
        """
        Get a ``value`` from a key ``name``

        :param name: str, name of the variable

        :return: bytes | str | None, the value as str or None if it doesn't exist
        """
        return self.redis.get(name)

    def increment_counter(self, name: str) -> int | Awaitable[int]:
        """
        Increment a Redis counter for the given name

        :param name: str, name of the counter
        :return: int, the updated counter value
        """
        return self.redis.incr(name)

    def get_counter(self, name: str) -> int:
        """
        Get the value of a Redis counter

        :param name: str, name of the counter
        :return: int, counter value (0 if missing)
        """
        return int(self.redis.get(name) or 0)

    def add_to_set(self, name: str, *values) -> int:
        """
        Add a value to a Redis set

        :param name: str, name of the set
        :param values: values to add to the set
        :return: int, number of elements added (0 or 1)
        """
        return self.redis.sadd(name, *values)

    def get_set(self, name: str) -> set:
        """
        Retrieve all members of a Redis set

        :param name: str, name of the set used
        :return: set[str], Set of stored values
        """
        return self.redis.smembers(name)

    def get_random_from_set(self, name: str) -> bytes | str | list[bytes | str] | None:
        """
        Retrieve a random member from a Redis set

        :param name: str, name of the set used
        :return: str, the random value
        """
        return self.redis.srandmember(name)

    def add_hash(self, name: str, mapping: dict) -> int:
        """
        Set a dictionary as a hash Redis in one go

        :param name: str, name of the hash used
        :param mapping: dict, the dictionary used

        :return: int, the number of fields that were added
        """
        return self.redis.hset(name, mapping=mapping)

    def get_from_hash(self, name: str, key: str) -> bytes | str | None:
        """
        Retrieve the value of key from a Redis hash

        :param name: str, name of the hash used
        :param key: str, key of the value to retrieve

        :return: bytes | str | None, the wanted value
        """
        return self.redis.hget(name, key=key)
