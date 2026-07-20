"""
Droping tables and types from the database
"""

from utilities.database import db_connection, DB_NAME, execute_query

def run(drop_only_library: bool = False) -> None:
    """
    Deletes all or selected tables from the database

    :param drop_only_library: bool, True if to drop only library schema's tables, False to remove all table

    :return: None
    """
    # ---------------------------------------------------------------------------------------
    # --- Set up Connection to Database ---

    # Establish connection
    connection = db_connection(database=DB_NAME)
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # --- Drop the Tables (if they already exist) ---

    # Drop sequence for the catalog schema
    drop_sequence_catalogue = [
        'catalog.' + table_name
        for table_name in [
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
    ]

    # Drop sequence for the library schema
    drop_sequence_library = [
        'library.' + table_name
        for table_name in [
            'fines',
            'reservations',
            'loans',
            'copies',
            'librarians',
            'users',
        ]
    ]

    # Setting final table drop sequence
    if drop_only_library:
        # If only the library schema is to be dropped then only its drop
        # sequence is used
        table_drop_sequence = drop_sequence_library
    else:
        # Else if all the tables are to be dropped then first the library
        # schema's drop sequence is used and then the catalog's
        table_drop_sequence = drop_sequence_library + drop_sequence_catalogue

    # Drop each table using the proper drop sequence
    for table_name in table_drop_sequence:
        execute_query(
            connection=connection,
            query=f"DROP TABLE IF EXISTS {table_name};",
        )
    # ---------------------------------------------------------------------------------------

    # ---------------------------------------------------------------------------------------
    # --- Drop the Types (if they already exist) ---

    # Drop sequence for the library schema's types
    drop_type_sequence = [
        'library.' + table_type
        for table_type in [
            'copy_status',
            'loan_status',
            'reservation_status',
            'fine_status',
        ]
    ]

    # Drop each type using the proper drop sequence
    for table_type in drop_type_sequence:
        execute_query(
            connection=connection,
            query=f"DROP TYPE IF EXISTS {table_type};",
        )
    # ---------------------------------------------------------------------------------------
