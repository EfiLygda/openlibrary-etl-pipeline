"""
Setting up project's directories
"""

from config.paths import *
from utilities.logger import set_logger

logger = set_logger('SETUP_DIRECTORIES')

# List containing all new directories
NEW_DIRS = [
    DATA_DIR,
    CSV_DIR,
    RAW_PAGES_DIR,
    GENRE_DIR,
    SEARCH_DIR,
    KEYS_DIR,
    WORKS_DIR,
    AUTHORS_DIR,
    SERIES_DIR,
    BOOKS_DIR,
    # PUBLISHERS_DIR,
    # SUBJECTS_DIR,
    AUTHORS_STATISTICS_DIR,
    WORKS_RATINGS_DIR,
    LOG_DIR,
]

def run():

    logger.info('STAGE_START')

    # Creating new directories, if they do not already exist
    for directory in NEW_DIRS:
        if not os.path.exists(directory):
            os.makedirs(directory)
            logger.info(f'DIRECTORY_CREATE_SUCCESS path={directory}')
        else:
            logger.debug(f'DIRECTORY_EXISTS path={directory}')

    logger.info('STAGE_COMPLETE')