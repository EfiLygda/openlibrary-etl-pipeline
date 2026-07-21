"""
STEP 3:
"""

import os
from config.paths import CSV_DIR
from utilities.database import DB_NAME, db_connection
from utilities.io import read_csv
from utilities.logger import set_logger

logger = set_logger('LOAD_TABLES_AT_DATABASE')

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
    # --- Set up Connection to Database ---

    # Find table names
    table_names = [
        'authors',
        'authors_alternative_names',
        'authors_statistics',
        'works',
        'authors_works',
        'works_ratings',
        'works_series',
        'works_availability',
        'works_subjects',
        'works_people',
        'works_places',
        'works_time_periods',
        'editions',
        'editions_contributors',
        'editions_publishing',
        'editions_contents',
        'editions_details'
    ]

    # Find CSV tables filenames
    csv_files = [
        os.path.join(CSV_DIR, f'{table_name}.csv')
        for table_name in table_names
    ]
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # --- Load the Tables ---

    for table_name, csv_filepath in zip(table_names, csv_files):

        df_columns = read_csv(csv_filepath).columns

        with open(csv_filepath, mode='r', encoding='utf-8') as file:
            cursor.copy_expert(
            f"""
                COPY catalog.{table_name} ({','.join(df_columns)})
                FROM STDIN
                WITH CSV HEADER
                """,
                file
            )

        logger.info(f'TABLE_LOAD_SUCCESS table={table_name}')
    # ---------------------------------------------------------------------------------------

    # Close the cursor
    cursor.close()

    # Close the connection
    connection.close()

    logger.info('STAGE_COMPLETE')
