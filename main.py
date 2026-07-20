"""
Application entry point.

Configures logging and executes the application workflows in order:
1. Project setup
2. ETL pipeline
3. Library simulation

Run:
    python -m main
"""

import os
from dotenv import load_dotenv

from config.paths import LOG_DIR
from utilities.logging import config_logger, set_logger

from setup.setup_project import run as setup_project
from data_pipeline.pipeline import run as etl
from library.library_simulation import run as library_simulation

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
log_filepath = os.path.join(LOG_DIR, 'project.log')

# Configure the logger (uses console and file for log records)
config_logger(filepath=log_filepath, level=LOG_LEVEL)

# Set up the logger with stage 'APPLICATION'
logger = set_logger(stage='APPLICATION')
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Run Application (with logging) ---

if __name__ == '__main__':

    logger.info('APPLICATION_START')

    # The pipeline
    setup_project(drop_only_library=True)
    # etl()
    library_simulation()

    logger.info('APPLICATION_COMPLETE')

# ----------------------------------------------------------------------------------
