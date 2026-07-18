"""
Run the ETL pipeline
"""

import os
import logging
from dotenv import load_dotenv

from config.paths import LOG_DIR
from utilities.logging import config_logger, set_logger

from data_pipeline.extract import run as run_extract
from data_pipeline.transform import run as run_transform
from data_pipeline.load import run as run_load

# ----------------------------------------------------------------------------------
# --- Load Environment Variables ---
# Load variables from the .env file to the environment
load_dotenv()

# Setting up the genre
LOG_LEVEL = os.getenv("LOG_LEVEL")
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Setting up logging ---

# Silencing 'urllib3' logging to level warning
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Log filepath
log_filepath = os.path.join(LOG_DIR, 'etl.log')

# Configure the logger (uses console and file for log records)
config_logger(filepath=log_filepath, level=LOG_LEVEL)

# Set up the logger with stage 'ETL'
logger = set_logger(stage='ETL')
# ----------------------------------------------------------------------------------

def run():
    # ----------------------------------------------------------------------------------
    # --- Run Pipeline (with logging) ---

    logger.info('PIPELINE_START')

    # The pipeline
    # run_extract()
    # run_transform()
    run_load()

    logger.info('PIPELINE_COMPLETE')
    # ----------------------------------------------------------------------------------

if __name__ == '__main__':
    run()