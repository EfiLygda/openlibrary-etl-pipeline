"""
Extract General Works, Editions and Authors' data using the OpenLibrary API to JSON files

Note: Refer to etl/extract/docs/api_documentation.md for keywords SEARCH, WORKS, AUTHORS, SERIES,
      SEARCH_EDITIONS_VIA_WORK_KEY, SEARCH_AUTHORS

Pipeline:
STEP 1: Extract first 2000 works under the genre via SEARCH
STEP 2: Extract all work keys, author keys, series keys,
STEP 3: Use OpenLibraryClient.get_many to extract via keys all WORKS, AUTHORS, SERIES
STEP 4: From author data extract author key, name pairs. This is done to use author's main name and
        remove pen names or other versions
STEP 5: Use SEARCH_EDITIONS_VIA_WORK_KEY to find and extract all editions in a work
STEP 6: Use OpenLibraryClient.get_many to extract via keys all BOOKS
Step 7: Extract all publishers, subjects, subject_people and subject_times via SEARCH_EDITIONS_VIA_WORK_KEY
Step 8: Extract all SEARCH_AUTHORS fields from SEARCH_AUTHORS
"""
import logging
import os.path

from config.paths import LOG_DIR

from utilities.logging import config_logger, set_logger

from etl.extract.fetch_works import run as fetch_works
from etl.extract.export_keys import run as export_keys
from etl.extract.fetch_works_authors_series import run as fetch_works_authors_series
from etl.extract.export_author_key_names import run as export_author_key_names
from etl.extract.fetch_books_keys_via_work_key import run as fetch_books_keys_via_work_key
from etl.extract.fetch_books import run as fetch_books
from etl.extract.export_publishers_subjects_people_times import run as export_publishers_subjects_people_times
from etl.extract.fetch_author_statistics import run as fetch_author_statistics

def run():
    # ----------------------------------------------------------------------------------
    # --- Setting up logging ---

    # Log filepath
    log_filepath = os.path.join(LOG_DIR, 'extract.log')

    # Configure the logger (uses console and file for log records)
    config_logger(filepath=log_filepath, level='info')

    # Set up the logger with stage 'EXTRACT'
    logger = set_logger(stage='EXTRACT')
    # ----------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------
    # --- Run Pipeline (with logging) ---

    logger.info('Started extraction of data from OpenLibrary API to JSON files')

    # The pipeline
    fetch_works()
    export_keys()
    fetch_works_authors_series()
    export_author_key_names()
    fetch_books_keys_via_work_key()
    fetch_books()
    export_publishers_subjects_people_times()
    fetch_author_statistics()

    logger.info('Finished extraction of data from OpenLibrary API to JSON files')

    # Shutting down logging
    logging.shutdown()
    # ----------------------------------------------------------------------------------

    # ----------------------------------------------------------------------------------
    # --- Run Pipeline (without logging) ---

    # import os
    # from config.paths import ROOT_DIR
    # from utilities.pipeline import run_pipeline
    # from utilities.logging import LOGGING_FORMAT, DATE_FORMAT

    # # Set up directory containing the pipeline py files
    # tasks_dir = os.path.join(ROOT_DIR, 'to_JSON')
    #
    # # The pipeline's py filenames for extracting JSON files via the API
    # tasks = [
    #     # 'fetch_works.py',
    #     # 'export_keys.py',
    #     # 'fetch_works_authors_series.py',
    #     # 'export_author_key_names.py',
    #     # 'fetch_books_keys_via_work_key.py',
    #     # 'fetch_books.py',
    #     # 'export_publishers_subjects_people_times.py',
    #     # 'fetch_author_statistics.py',
    # ]
    #
    # # Run the pipeline
    # run_pipeline(
    #     tasks_dir=tasks_dir,
    #     tasks=tasks
    # )
    # ----------------------------------------------------------------------------------
