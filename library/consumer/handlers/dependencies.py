"""
Provides shared dependencies required by event handlers
"""

import psycopg2
from typing import Optional
from dataclasses import dataclass

from kafka import KafkaProducer

from library.service.redis.operations.registry import RedisOperations

@dataclass
class HandlerDependencies:
    """
    Provides shared dependencies required by event handlers.

    :param connection: psycopg2.extensions.connection, connection used for database operations
    :param redis_operations: RedisOperations, Redis operations facade used for Redis state changes
    :param producer: KafkaProducer | None, Kafka producer used for emitting chain events
        when needed
    """

    connection: psycopg2.extensions.connection
    redis_operations: RedisOperations
    producer: Optional[KafkaProducer] = None
