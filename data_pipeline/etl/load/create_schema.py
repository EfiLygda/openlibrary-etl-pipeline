"""
STEP 2: Create the `catalog` schema
"""

from utilities.database import DB_NAME, db_connection, execute_query
from utilities.logger import set_logger

logger = set_logger('CREATE_ETL_SCHEMA')

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
        query='CREATE SCHEMA IF NOT EXISTS catalog;'
    )

    logger.info('SCHEMA_CREATE_SUCCESS schema=catalog')
    # ---------------------------------------------------------------------------------------

    # Close the connection
    connection.close()

    logger.info('STAGE_COMPLETE')
