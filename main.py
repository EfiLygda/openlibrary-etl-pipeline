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
import argparse
from dotenv import load_dotenv

from config.paths import LOG_DIR
from utilities.logger import config_logger, set_logger

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
log_filepath = os.path.join(LOG_DIR, 'application.log')

# Configure the logger (uses console and file for log records)
config_logger(filepath=log_filepath, level=LOG_LEVEL, reset_file=True)

# Set up the logger with stage 'APPLICATION'
logger = set_logger(stage='APPLICATION')
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Setting up command line argument parser ---

# Setting up argument parser via the command line
parser = argparse.ArgumentParser()

# Add `drop-only-library` flag for dropping only library schema
parser.add_argument(
    "--drop-only-library",
    action="store_true",
    help="Drop only library schema"
)

# Add `display-events` flag for displaying full event envelope in console
parser.add_argument(
    "--display-events",
    action="store_true",
    help="Display Kafka events during simulation"
)
# ----------------------------------------------------------------------------------


if __name__ == '__main__':

    # Parse command line arguments
    args = parser.parse_args()

    # ----------------------------------------------------------------------------------
    # --- Run Application (with logging) ---

    logger.info('APPLICATION_START')

    # The pipeline
    setup_project(drop_only_library=args.drop_only_library)
    # etl()
    library_simulation(display_events=args.display_events)

    logger.info('APPLICATION_COMPLETE')
    # ----------------------------------------------------------------------------------
