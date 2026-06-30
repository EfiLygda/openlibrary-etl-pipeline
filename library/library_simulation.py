"""
Central simulation of library data module
"""

import os
from dotenv import load_dotenv

from config.paths import LOG_DIR
from utilities.logging import config_logger, set_logger

from library.simulators.users import run as users
from library.simulators.librarians import run as librarians
from library.simulators.edition_copies import run as copies
from library.simulators.borrowings import run as borrowings

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
log_filepath = os.path.join(LOG_DIR, 'library.log')

# Configure the logger (uses console and file for log records)
config_logger(filepath=log_filepath, level=LOG_LEVEL)

# Set up the logger with stage 'LIBRARY'
logger = set_logger(stage='LIBRARY')
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- Run Pipeline (with logging) ---

logger.info('PIPELINE_START')

# The pipeline
users()
librarians()
copies()
borrowings()

logger.info('PIPELINE_COMPLETE')
# ----------------------------------------------------------------------------------

