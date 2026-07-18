"""
Load tables to romance_fiction PostgreSQL database
"""
from utilities.logging import set_logger

from data_pipeline.etl.load.create_database import run as create_database
from data_pipeline.etl.load.create_schema import run as create_schema
from data_pipeline.etl.load.create_tables import run as create_tables
from data_pipeline.etl.load.load_tables import run as load_tables
from data_pipeline.etl.load.create_indexes import run as create_indexes

def run():
    # ----------------------------------------------------------------------------------
    # --- Setting up logging ---

    # Log filepath
    # log_filepath = os.path.join(LOG_DIR, 'load.log')

    # Configure the logger (uses console and file for log records)
    # config_logger(filepath=log_filepath, level='info')

    # Set up the logger with stage 'EXTRACT'
    logger = set_logger(stage='LOAD')
    # ----------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------
    # --- Run Pipeline (with logging) ---

    logger.info('PHASE_START')

    # The pipeline
    create_database()
    create_schema()
    create_tables()
    load_tables()
    create_indexes()

    logger.info('PHASE_COMPLETE')
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
