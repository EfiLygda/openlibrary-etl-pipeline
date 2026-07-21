"""
Pipeline for setting up the project

* Create directories
* Clean database (drop ta tables and types)
"""

from utilities.logger import set_logger

from setup.create_directories import run as create_directories
from setup.clean_database import run as clean_database

logger = set_logger(stage='SETUP_PROJECT')

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
