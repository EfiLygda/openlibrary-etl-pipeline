"""
Transform JSON files to tables (CSV files)
1. authors.csv
2. authors_alternative_names.csv
3. authors_statistics.csv
4. authors_works.csv
5. editions.csv
6. editions_contents.csv
7. editions_contributors.csv
8. editions_details.csv
9. editions_publishing.csv
10. works.csv
11. works_availability.csv
12. works_people.csv
13. works_places.csv
14. works_series.csv
15. works_subjects.csv
16. works_time_periods.csv
"""

import os

from config.paths import LOG_DIR
from utilities.logging import config_logger, set_logger

from to_CSV.author_tables import run as author_tables
from to_CSV.editions_tables import run as editions_tables
from to_CSV.works_tables import run as works_tables

# ----------------------------------------------------------------------------------
# --- Setting up logging ---

# Log filepath
log_filepath = os.path.join(LOG_DIR, 'transform.log')

# Configure the logger (uses console and file for log records)
config_logger(filepath=log_filepath, level='info')

# Set up the logger with stage 'EXTRACT'
logger = set_logger(stage='TRANSFORM')
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Run Pipeline (with logging) ---

logger.info('Started transformation of data from JSON files to CSV files')

# The pipeline
author_tables()
editions_tables()
works_tables()

logger.info('Finished transformation of data from JSON files to CSV files')
# ----------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------
# --- Run Pipeline (without logging) ---
#
# from config.paths import ROOT_DIR
# from utilities.pipeline import run_pipeline
#
# # Set up directory containing the pipeline py files
# tasks_dir = os.path.join(ROOT_DIR, 'to_CSV')
#
# # The pipeline's py filenames for preprocessing and saving to CSV tables
# tasks = [
#     "author_tables.py",
#     "editions_tables.py",
#     "works_tables.py",
# ]
#
# # Run the pipeline
# run_pipeline(
#     tasks_dir=tasks_dir,
#     tasks=tasks
# )
# ----------------------------------------------------------------------------------
