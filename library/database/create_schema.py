"""
Create the `library` schema
"""

from utilities.database import DB_NAME, db_connection, execute_query
from utilities.logging import set_logger

logger = set_logger('CREATE_SCHEMA_AT_DATABASE')

def run():

    logger.info('STAGE_START')

    # ---------------------------------------------------------------------------------------
    # --- Set up Connection to Database ---

    # Establish connection
    connection = db_connection(database=DB_NAME)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # --- Create Schema ---
    execute_query(
        connection=connection,
        query='CREATE SCHEMA IF NOT EXISTS library;'
    )
    # ---------------------------------------------------------------------------------------

    # Close the connection
    connection.close()

    logger.info('STAGE_COMPLETE')
