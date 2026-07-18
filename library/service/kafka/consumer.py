"""
Kafka system factory utilities.

This module provides functions for creating and configuring Kafka system
instances used by the application to consume events from Kafka topics.
"""

import json
from kafka import KafkaConsumer
from library.service.kafka.config import BOOTSTRAP


def create_consumer(
        topic: str,
        group_id: str
) -> KafkaConsumer:
    """
    Create and configure a Kafka system instance

    The system subscribes to the provided topic and belongs to the
    specified system group

    :param topic: str, the Kafka topic to consume events from.
    :param group_id: str, the Kafka system group identifier.
    :return: KafkaConsumer, the configured Kafka system instance.
    """
    return KafkaConsumer(
        topic,
        bootstrap_servers=BOOTSTRAP,
        group_id=group_id,
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )