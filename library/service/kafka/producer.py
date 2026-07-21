"""
Kafka producer factory utilities

This module provides functions for creating and configuring Kafka producer
instances used by the application to publish events.
"""

import json
from typing import List, Tuple

from kafka import KafkaProducer
from kafka.serializer import Serializer
from library.service.kafka.config import BOOTSTRAP

class JsonSerializer(Serializer):

    def serialize(
            self,
            topic: str,
            headers: List[Tuple[str, bytes]],
            data: dict,
    ):
        """
        Serialize a message value into UTF-8 encoded JSON bytes.

        :param topic: str, Kafka topic the message is being published to.
        :param headers: List[Tuple[str, bytes]], header for event's metadata.
        :param data: dict, dictionary containing the event payload.

        :return: Serialized message as UTF-8 encoded bytes.
        """
        return json.dumps(data).encode("utf-8")

def create_producer() -> KafkaProducer:
    """
    Create and configure a Kafka producer instance.

    The producer serializes event dictionaries into JSON format and connects
    to the configured Kafka bootstrap servers.

    :return: KafkaProducer, the configured Kafka producer instance.
    """
    return KafkaProducer(
        bootstrap_servers=BOOTSTRAP,
        value_serializer=JsonSerializer()
    )