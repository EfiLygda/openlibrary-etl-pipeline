"""
Create the tables at the database

Details: Tables are created with this sequence:

"""
import os

from config.paths import LIBRARY_SCHEMA

from utilities.database import DB_NAME, db_connection
from data_pipeline.utils.data.validation import check_if_table_exists
from utilities.logging import set_logger

logger = set_logger('CREATE_TABLES_AT_DATABASE')

def run():

    logger.info('STAGE_START')

    # ---------------------------------------------------------------------------------------
    # --- Set up Connection to Database ---

    # Establish connection
    connection = db_connection(database=DB_NAME)

    # Set up cursor
    cursor = connection.cursor()
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # --- Create Tables ---

    # List with the right sequence of sql files containing the CREATE command for each table
    table_sql_paths = [
        os.path.join(LIBRARY_SCHEMA, filename)
        for filename in sorted(os.listdir(LIBRARY_SCHEMA))
    ]

    # For each table sql CREATE file create the table if it does not already exist
    for table_path in table_sql_paths:

        # Extract the table name from the filepath
        table_name = os.path.basename(table_path).replace('.sql', '')[3:]

        # Check if the table already exists (this is mainly for logging)
        table_exists = check_if_table_exists(
            cursor,
            table_name=table_name,
            logger=logger
        )

        # Read the SQL command and execute it
        with open(table_path, encoding='utf-8', mode='r') as f:
            sql = f.read()
            cursor.execute(sql)

            if not table_exists:
                logger.info(f'TABLE_CREATE_SUCCESS table={table_name}')

    # Close the cursor
    cursor.close()

    # Close the connection
    connection.close()

    logger.info('STAGE_COMPLETE')
