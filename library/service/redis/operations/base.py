"""
Base class for Redis state operation handlers.
"""

from library.service.redis.client import RedisClient

class RedisOperationsBase:
    """
    Base class for Redis state operation handlers.

    Stores the Redis client instance used by subclasses to perform
    state reads and mutations.

    :param redis_client: RedisClient, the Redis client used for accessing
        and modifying the library's Redis state
    """
    def __init__(self, redis_client: RedisClient):
        self.client = redis_client
