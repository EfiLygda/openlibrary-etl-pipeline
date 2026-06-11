"""
STEP 1: Create `romance_fiction` database
"""
from config import GENRE_facet
from utilities.database import db_connection
from utilities.logging import set_logger

logger = set_logger('CREATE_DATABASE')

def run():

    logger.info('STAGE_START')

    # ---------------------------------------------------------------------------------------
    # --- Set up Connection to Database ---

    # Establish connection
    connection = db_connection()

    # Set up cursor
    cursor = connection.cursor()
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # --- Create Database (if it does not exist) ---

    # Check if database already exists and then create
    # Source: https://stackoverflow.com/a/44512503
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'openlibrary_db';")
    exists = cursor.fetchone()
    if not exists:
        logger.warning(f'DATABASE_NOT_FOUND database={GENRE_facet}')
        cursor.execute('CREATE DATABASE openlibrary_db;')
        logger.info(f'DATABASE_CREATE_SUCCESS database={GENRE_facet}')
    else:
        logger.info(f'DATABASE_EXISTS database={GENRE_facet}')

    # Close the cursor
    cursor.close()

    # Close the connection
    connection.close()

    logger.info('STAGE_COMPLETE')
    # ---------------------------------------------------------------------------------------