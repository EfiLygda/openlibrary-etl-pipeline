"""
Central simulation of the library
"""

import os
import logging
from dotenv import load_dotenv

from utilities.logger import set_logger

from library.setup.create_tables import run as create_tables
from library.setup.create_schema import run as create_schema
from library.setup.reset_kafka_topic import run as reset_kafka_topic
from library.setup.init_redis_state import run as initialize_redis_state
from library.setup.start_library import run as start_library

# ----------------------------------------------------------------------------------
# --- Load Environment Variables ---
# Load variables from the .env file to the environment
load_dotenv()

# Setting up the genre
LOG_LEVEL = os.getenv("LOG_LEVEL")
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Setting up logging ---

# Silencing 'redis' logging to level 'WARNING'
logging.getLogger("redis").setLevel(logging.WARNING)
logging.getLogger("redis.connection").setLevel(logging.WARNING)
logging.getLogger("redis.client").setLevel(logging.WARNING)

# Silencing 'kafka' logging to level 'WARNING'
logging.getLogger("kafka").setLevel(logging.WARNING)

# # Log filepath
# log_filepath = os.path.join(LOG_DIR, 'library.log')
#
# # Configure the logger (uses console and file for log records)
# config_logger(filepath=log_filepath, level=LOG_LEVEL)

# Set up the logger with stage 'SIMULATE_LIBRARY'
logger = set_logger(stage='SIMULATE_LIBRARY')
# ----------------------------------------------------------------------------------

def run(display_events: bool = False) -> None:
    """
    Runs the complete library simulation pipeline.

    The pipeline resets the Kafka topic, initializes the database schema and
    tables, generates the initial simulation data, and starts the library
    event processing system. The simulation continues until interrupted.

    Pipeline steps:
        1. Reset the Kafka topic used for library events.
        2. Create the database schema.
        3. Create the required database tables.
        4. Initialize simulation data and publish initial events.
        5. Start the library system consumer and producer.

    :param display_events: Whether to display full event payloads during the
        simulation.
    :return: None
    """

    # ----------------------------------------------------------------------------------
    # --- Run Pipeline (with logging) ---

    logger.info('PIPELINE_START')
    #TODO: add drop database and schemas

    # The pipeline
    reset_kafka_topic()
    create_schema()
    create_tables()
    initialize_redis_state()
    start_library(display_events=display_events)

    logger.info('PIPELINE_COMPLETE')
    # ----------------------------------------------------------------------------------
