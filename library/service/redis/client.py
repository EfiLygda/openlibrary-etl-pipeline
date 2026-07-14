"""
Redis service wrapper module.

Provides a simplified interface around Redis commands used by the library
system. The module groups Redis operations by data structure type while
sharing a single Redis connection.

Available wrappers:
- RedisDatabase: Database-level operations such as flushing and key counts.
- RedisInspection: Redis introspection and key metadata operations.
- RedisString: String key operations.
- RedisCounter: Numeric counter operations.
- RedisHash: Hash data structure operations.
- RedisSet: Set data structure operations.
- RedisQueue: List-based queue operations.

RedisClient acts as the main entry point and exposes each operation group
through dedicated attributes.
"""

from typing import Awaitable, Any

import redis
from redis.client import Pipeline

from library.service.redis.config import REDIS_HOST, REDIS_PORT

class _RedisBase:
    """
    Shared Redis client configuration and helpers
    """

    def __init__(self, redis_connection: redis.client.Redis):
        self.redis = redis_connection

class _RedisDatabase(_RedisBase):
    """
    Provides Redis database management operations
    """

    def flush(self) -> None:
        """
        Delete all keys in the current Redis database
        """
        self.redis.flushdb()

    def get_size(self) -> int:
        """
        Retrieve total number of keys in database

        :return: int, number of stored keys
        """
        return self.redis.dbsize()

class _RedisInspection(_RedisBase):
    """
    Provides Redis key inspection operations
    """

    def get_all_keys(self):
        """
        Retrieve all keys from current Redis database

        :return: iterator, Redis keys
        """
        return self.redis.scan_iter()

    def get_type(self, name: str) -> bytes | str:
        """
        Retrieve Redis data type of key

        :param name: str, Redis key name
        :return: str, Redis data type
        """
        return self.redis.type(name)

    def get_memory_usage(self, name: str) -> int | None:
        """
        Retrieve memory usage of Redis key

        :param name: str, Redis key name
        :return: int, memory usage in bytes
        """
        return self.redis.memory_usage(name)

class _RedisString(_RedisBase):
    """
    Provides Redis string value operations
    """

    def set(self, name: str, value: int | str) -> bool | str | bytes | None:
        """
        Set a ``value`` to key ``name``

        :param name: str, name of the variable
        :param value: str, value of the variable

        :return: bool | str | bytes | None, whether the value was set or not
        """
        return self.redis.set(name, value)

    def get(self, name: str) -> bytes | str | None:
        """
        Get a ``value`` from a key ``name``

        :param name: str, name of the variable

        :return: bytes | str | None, the value as str or None if it doesn't exist
        """
        return self.redis.get(name)

    def get_length(self, name: str) -> int:
        """
        Get the length of the string value stored at key ``name``.

        :param name: str, name of the key

        :return: int, length of the stored string value (0 if the key does not exist)
        """
        return self.redis.strlen(name)

class _RedisSet(_RedisBase):
    """
    Provides Redis set data structure operations
    """

    def add(self, name: str, *values) -> int:
        """
        Add a value to a Redis set

        :param name: str, name of the set
        :param values: values to add to the set
        :return: int, number of elements added (0 or 1)
        """
        return self.redis.sadd(name, *values)

    def get(self, name: str) -> set:
        """
        Retrieve all members of a Redis set

        :param name: str, name of the set used
        :return: set[str], Set of stored values
        """
        return self.redis.smembers(name)

    def get_size(self, name: str) -> int:
        """
        Retrieve the size of a Redis set

        :param name: str, name of the set
        :return: int, the size of the set
        """
        return self.redis.scard(name)

    def random(self, name: str) -> bytes | str | list[bytes | str] | None:
        """
        Retrieve a random member from a Redis set

        :param name: str, name of the set used
        :return: str, the random value
        """
        return self.redis.srandmember(name)

    def move(self, source: str, destination: str, value: str | int) -> bool | Awaitable[bool]:
        """
        Move value from a Redis set to another

        :param source: str, name of the source set
        :param destination: str, name of the destination set
        :param value: str | int, value to be moved

        :return: bool, True if the value was moved, 0 if not
        """

        return self.redis.smove(source, destination, value)

    def remove(self, name: str, *values) -> int:
        """
        Remove values from a Redis set

        :param name: str, name of the set
        :param values: values to remove from the set
        :return: int, 1 if the value was removed or 0 if not
        """
        return self.redis.srem(name, *values)

class _RedisCounter(_RedisBase):
    """
    Provides Redis counter operations
    """

    def get(
            self,
            name: str,
            key: str | None = None
    ) -> int:
        """
        Get the value of a Redis counter or hash counter field

        :param name: Redis key (or hash name)
        :param key: Hash field name. If None, `name` is treated as a normal key.
        :return: Counter value (0 if missing)
        """
        if key is None:
            value = self.redis.get(name)
        else:
            value = self.redis.hget(name, key)

        return int(value or 0)

    def increment(
            self,
            name: str,
            key: str | None = None,
    ) -> int | Awaitable[int]:
        """
        Increment a Redis counter or hash counter field

        :param name: str, Redis key (or hash name)
        :param key: str | None, Hash field name. If None, increment the key itself
        :return: Updated counter value
        """

        if key is None:
            return self.redis.incr(name)

        return self.redis.hincrby(name, key, 1)

class _RedisHash(_RedisBase):
    """
    Provides Redis hash data structure operations
    """

    def set_mapping(self, name: str, mapping: dict) -> int:
        """
        Set a dictionary as a hash Redis in one go

        :param name: str, name of the hash used
        :param mapping: dict, the dictionary used

        :return: int, number of new fields added to the hash
        """
        return self.redis.hset(name, mapping=mapping)

    def set(self, name: str, key: str, value: int | str) -> int:
        """
        Set the value of a key from a Redis hash

        :param name: str, name of the hash used
        :param key: str, key of the value to retrieve
        :param value: str, the value to set

        :return: int, number of fields added (1 for a new field, 0 for an updated field)
        """
        return self.redis.hset(name=name, key=key, value=value)

    def get(self, name: str, key: str) -> bytes | str | None:
        """
        Retrieve the value of key from a Redis hash

        :param name: str, name of the hash used
        :param key: str, key of the value to retrieve

        :return: bytes | str | None, the wanted value
        """
        return self.redis.hget(name, key=key)

    def get_length(self, name: str) -> int:
        """
        Get the number of fields stored in a Redis hash.

        :param name: str, name of the hash used

        :return: int, number of fields in the hash
        """
        return self.redis.hlen(name)

class _RedisQueue(_RedisBase):
    """
    Provides Redis queue operations using Redis lists
    """

    def add(self, name: str, *values):
        """
        Append one or more values to the end of a Redis list

        :param name: str, name of the Redis list
        :param values: one or more values to push into the list

        :return: int, the length of the list after the push operation
        """
        return self.redis.rpush(name, *values)

    def get_length(self, name: str) -> int:
        """
        Get the number of elements in a Redis list

        :param name: str, name of the Redis list
        :return: int, number of elements currently stored in the list
        """
        return self.redis.llen(name)

    def pop(self, name: str) -> bytes | str | list[bytes | str] | None:
        """
        Remove and return the first element of a Redis list

        :param name: str, name of the Redis list to pop from

        :return: bytes | str | None, the popped value from the list,
                 or None if the list does not exist or is empty
        """
        return self.redis.lpop(name)

    def remove(self, name: str, value: Any) -> int:
        """
        Removes a value from a Redis list

        :param name: str, name of the Redis list
        :param value: str, value to remove

        :return: int, number of removed elements
        """
        # If count = 0 then all occurrences of the value are removed
        return self.redis.lrem(name=name, count=0, value=value)

class RedisClient:
    """
    Provides a high-level interface for Redis operations used by the library system
    """

    def __init__(self, database: int = 0):

        connection = redis.Redis(
            host=REDIS_HOST,
            port=REDIS_PORT,
            db=database,
            decode_responses=True  # Returns strings instead of bytes
        )

        self.redis = connection

        self.database = _RedisDatabase(connection)
        self.inspection = _RedisInspection(connection)

        self.strings = _RedisString(connection)
        self.counters = _RedisCounter(connection)
        self.hashes = _RedisHash(connection)
        self.sets = _RedisSet(connection)
        self.queues = _RedisQueue(connection)

    def close(self) -> None:
        """
        Close the client connection
        """
        self.redis.close()

    def pipeline(self) -> Pipeline:
        """
        Redis pipeline for queuing multiple commands for later execution
        """
        return self.redis.pipeline()
