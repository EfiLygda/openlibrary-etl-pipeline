"""
Kafka producer factory utilities

This module provides functions for creating and configuring Kafka producer
instances used by the application to publish events.
"""

import json
from kafka import KafkaProducer
from library.service.kafka.config import BOOTSTRAP

def create_producer() -> KafkaProducer:
    """
    Create and configure a Kafka producer instance.

    The producer serializes event dictionaries into JSON format and connects
    to the configured Kafka bootstrap servers.

    :return: KafkaProducer, the configured Kafka producer instance.
    """
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        value_serializer=lambda v: json.dumps(v).encode("utf-8")
    )