"""
Central simulation of the library
"""

import os
from dotenv import load_dotenv
import logging

from config.paths import LOG_DIR
from utilities.logging import config_logger, set_logger

from library.database.create_tables import run as create_tables
from library.database.create_schema import run as create_schema
from library.setup.reset_kafka_topic import run as reset_kafka_topic
from library.producer.simulation.init_simulation import run as initialize_simulation
from library.start_library import run as start_library

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

# Log filepath
log_filepath = os.path.join(LOG_DIR, 'library.log')

# Configure the logger (uses console and file for log records)
config_logger(filepath=log_filepath, level=LOG_LEVEL)

# Set up the logger with stage 'LIBRARY_SIMULATION'
logger = set_logger(stage='LIBRARY_SIMULATION')
# ----------------------------------------------------------------------------------

def run():
    # ----------------------------------------------------------------------------------
    # --- Run Pipeline (with logging) ---

    logger.info('PIPELINE_START')

    # The pipeline
    reset_kafka_topic()
    create_schema()
    create_tables()
    initialize_simulation()
    start_library()

    logger.info('PIPELINE_COMPLETE')
    # ----------------------------------------------------------------------------------
