"""
STEP 4:
"""

import os
import re

from config.paths import INDEXES_DIR

from utilities.database import DB_NAME, db_connection
from utilities.data.validation import check_if_index_exists
from utilities.logging import set_logger

logger = set_logger('CREATE_INDEXES_AT_DATABASE')

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
    # --- Create Indexes ---

    # List with the SQL files containing the CREATE INDEX command for each table
    indexes_sql_paths = [
        os.path.join(INDEXES_DIR, filename)
        for filename in os.listdir(INDEXES_DIR)
    ]

    # For each table sql CREATE file create the table if it does not already exist
    for index_path in indexes_sql_paths:

        # Extract the table name from the filepath
        table_name = os.path.basename(index_path).replace('.sql', '')

        # Read the SQL command and execute it
        with open(index_path, encoding='utf-8', mode='r') as f:
            sql = f.read()

            index_name_pattern = r'CREATE\s+INDEX\s+(?:IF\s+NOT\s+EXISTS\s+)?([a-zA-Z0-9_]+)\s+ON'
            indexes_names = re.findall(index_name_pattern, sql)

            # Check if the index already exists (this is mainly for logging)
            indexes_exists = [
                check_if_index_exists(
                    cursor,
                    index_name=index_name,
                    logger=logger
                )
                for index_name in indexes_names
            ]

            cursor.execute(sql)

            for index_name, index_exists in zip(indexes_names, indexes_exists):
                if not index_exists:
                    logger.info(f'INDEXES_CREATE_SUCCESS table={table_name} index={index_name}')

    # Close the cursor
    cursor.close()

    # Close the connection
    connection.close()

    logger.info('STAGE_COMPLETE')