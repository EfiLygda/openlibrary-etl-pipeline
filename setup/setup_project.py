"""
Pipeline for setting up the project

* Create directories
* Clean database (drop ta tables and types)
"""

import os
from dotenv import load_dotenv

from config.paths import LOG_DIR
from utilities.logger import config_logger, set_logger

from setup.create_directories import run as create_directories
from setup.clean_database import run as clean_database

# ----------------------------------------------------------------------------------
# --- Load Environment Variables ---
# Load variables from the .env file to the environment
load_dotenv()

# Setting up the genre
LOG_LEVEL = os.getenv("LOG_LEVEL")
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Setting up logging ---

# Log filepath
log_filepath = os.path.join(LOG_DIR, 'setup.log')

# Configure the logger (uses console and file for log records)
config_logger(filepath=log_filepath, level=LOG_LEVEL)

# Set up the logger with stage 'SETUP'
logger = set_logger(stage='SETUP_PROJECT')
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Run Pipeline (with logging) ---

def run(drop_only_library: bool = True) -> None:
    """
    Deletes all or selected tables from the database

    :param drop_only_library: bool, True if to drop only library schema's tables, False to remove all table

    :return: None
    """

    logger.info('PHASE_START')

    # The pipeline
    create_directories()
    clean_database(drop_only_library=drop_only_library)

    logger.info('PHASE_COMPLETE')

# ----------------------------------------------------------------------------------
