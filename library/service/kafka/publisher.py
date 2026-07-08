"""
Kafka event publishing utilities

This module provides helper functions for publishing application events
to Kafka topics using configured Kafka producer instances.
"""

import kafka

def emit_event(
        producer: kafka.producer.kafka.KafkaProducer,
        topic: str,
        event: dict
) -> None:
    """
    Publish an event to the configured Kafka topic

    The event is sent asynchronously to the configured topic and then
    immediately flushed to ensure it is available to consumers

    :param producer: kafka.producer.kafka.KafkaProducer, the Kafka producer
        instance used to publish the event
    :param topic: str, the Kafka topic to publish the event to
    :param event: dict, the event dictionary to publish

    :return: None.
    """
    # Publish the allowed event to chosen topic
    producer.send(topic, value=event)

    # All buffered events are immediately available
    # TODO: add batches
    producer.flush()