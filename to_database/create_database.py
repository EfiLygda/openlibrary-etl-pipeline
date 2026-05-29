"""
STEP 1: Create `romance_fiction` database
"""
from config import GENRE_facet
from utilities.database import db_connection
from utilities.logging import set_logger

logger = set_logger('CREATE_DATABASE')

def run():

    logger.info('Started creation of database')

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
    cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'romance_fiction';")
    exists = cursor.fetchone()
    if not exists:
        logger.warning(f'Database \'{GENRE_facet}\' does not exist -> it will be created')
        cursor.execute('CREATE DATABASE romance_fiction;') # Did not inject GENRE_facet to SQL
    else:
        logger.warning(f'Database \'{GENRE_facet}\' already exists')

    # Close the cursor
    cursor.close()

    # Close the connection
    connection.close()

    logger.info('Finished creation of database')
    # ---------------------------------------------------------------------------------------