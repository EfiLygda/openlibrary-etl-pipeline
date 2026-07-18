"""
STEP 2: Create the tables at `romance_fiction` database

Details: Tables are created with this sequence:
1. authors
2. authors_alternative_names
3. authors_statistics
4. works
5. authors_works
6. works_ratings
7. works_series
8. works_availability
9. works_subjects
10. works_people
11. works_places
12. works_time_periods
13. editions
14. editions_contributors
15. editions_publishing
16. editions_contents
17. editions_details
"""
import os

from config.paths import SCHEMA_DIR

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
    # --- Drop the Tables (if they already exist)

    drop_sequence = [
        'authors_alternative_names',
        'authors_statistics',
        'authors_works',

        'authors',

        'works_ratings',
        'works_series',
        'works_availability',
        'works_subjects',
        'works_people',
        'works_places',
        'works_time_periods',

        'editions_contributors',
        'editions_publishing',
        'editions_contents',
        'editions_details',
        'editions',

        'works',
    ]

    for table_name in drop_sequence:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name};")
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # --- Create Tables ---

    # List with the right sequence of sql files containing the CREATE command for each table
    table_sql_paths = [
        os.path.join(SCHEMA_DIR, filename)
        for filename in sorted(os.listdir(SCHEMA_DIR))
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
