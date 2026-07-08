"""
Kafka consumer factory utilities.

This module provides functions for creating and configuring Kafka consumer
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
    Create and configure a Kafka consumer instance

    The consumer subscribes to the provided topic and belongs to the
    specified consumer group

    :param topic: str, the Kafka topic to consume events from.
    :param group_id: str, the Kafka consumer group identifier.
    :return: KafkaConsumer, the configured Kafka consumer instance.
    """
    return KafkaConsumer(
        topic,
        bootstrap_servers=BOOTSTRAP,
        group_id=group_id,
        value_deserializer=lambda v: json.loads(v.decode("utf-8"))
    )