"""
Recreates the Kafka topic used by the application.

The existing topic is deleted if it exists and then created again using the
configured Kafka broker and topic settings.
"""

import os
from dotenv import load_dotenv
from utilities.command import run_command
from utilities.logger import set_logger

# Load variables from the .env file to the environment
load_dotenv()

# Load the variables
TOPIC = str(os.getenv('TOPIC'))
BOOTSTRAP = str(os.getenv('BOOTSTRAP'))
KAFKA_CONTAINER = str(os.getenv('KAFKA_CONTAINER'))
KAFKA_TOPICS = str(os.getenv('KAFKA_TOPICS'))

logger = set_logger('RESET_KAFKA_TOPIC')

def run():
    """
    Recreates the configured Kafka topic.

    If the topic already exists, it is deleted before being created again with
    the configured number of partitions and replication factor.

    :return: None
    """

    logger.info('STAGE_START')

    # Delete topic and ignore if it doesn't exist
    run_command([
        'docker', 'exec', KAFKA_CONTAINER,
        KAFKA_TOPICS,
        '--bootstrap-server', BOOTSTRAP,
        '--delete',
        '--topic', TOPIC
    ], ignore_errors=True)

    # Create the topic
    run_command([
        'docker', 'exec', KAFKA_CONTAINER,
        KAFKA_TOPICS,
        '--bootstrap-server', BOOTSTRAP,
        '--create',
        '--topic', TOPIC,
        '--partitions', '1',
        '--replication-factor', '1'
    ])

    logger.info(f'TOPIC_CREATE_SUCCESS topic={TOPIC}')

    logger.info('STAGE_COMPLETE')