"""
Load tables to romance_fiction PostgreSQL database
"""


import os

from config.paths import LOG_DIR
from utilities.logging import config_logger, set_logger

from etl.load.create_database import run as create_database
from etl.load.create_tables import run as create_tables
from etl.load.load_tables import run as load_tables

# ----------------------------------------------------------------------------------
# --- Setting up logging ---

# Log filepath
log_filepath = os.path.join(LOG_DIR, 'load.log')

# Configure the logger (uses console and file for log records)
config_logger(filepath=log_filepath, level='info')

# Set up the logger with stage 'EXTRACT'
logger = set_logger(stage='LOAD')
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Run Pipeline (with logging) ---

logger.info('Started loading data to database')

# The pipeline
create_database()
create_tables()
load_tables()

logger.info('Finished loading data to database')
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Run Pipeline (without logging) ---

# import os
# from config.paths import ROOT_DIR
# from utilities.pipeline import run_pipeline
#
# # Set up directory containing the pipeline py files
# tasks_dir = os.path.join(ROOT_DIR, 'to_database')
#
# # The pipeline's py filenames for extracting JSON files via the API
# tasks = [
#     'create_database.py',
#     'create_tables.py',
#     'load_tables.py'
# ]
#
# # Run the pipeline
# run_pipeline(
#     tasks_dir=tasks_dir,
#     tasks=tasks
# )
# ----------------------------------------------------------------------------------
