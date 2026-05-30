"""
Run the ETL pipeline
"""

import os

from config.paths import LOG_DIR
from utilities.logging import config_logger, set_logger

from init_project import run as init_project
from extract import run as run_extract
from transform import run as run_transform
from load import run as run_load

# ----------------------------------------------------------------------------------
# --- Setting up logging ---

# Log filepath
log_filepath = os.path.join(LOG_DIR, 'etl.log')

# Configure the logger (uses console and file for log records)
config_logger(filepath=log_filepath, level='info')

# Set up the logger with stage 'ETL'
logger = set_logger(stage='ETL')
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Run Pipeline (with logging) ---

logger.info('Started ETL process')

# The pipeline
init_project()
run_extract()
run_transform()
run_load()

logger.info('Finished ETL process')
# ----------------------------------------------------------------------------------
