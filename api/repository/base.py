"""
get_by_entity_key that retrieves records from a given table in the database by its entity key

Notes:
1. 'entity key' is not primary key for each table but only for the three main
tables `works`, `authors` and `editions`
2. psycopg2.sql.SQL is used in order to make a query template
   using a certain table, its column names and entity's key
3. psycopg2.sql.Identifier is used for safe injection
"""

import psycopg2
from psycopg2.sql import SQL, Identifier

from utilities.database import get_column_names

SELECT_FROM_TABLE_TEMPLATE = SQL('SELECT {} FROM {}')
SELECT_FROM_TABLE_WITH_FILTER_TEMPLATE = SQL('SELECT {} FROM {} WHERE {} = %s')

SELECT_FROM_JOINED_TABLES_WITHOUT_FILTER_TEMPLATE = SQL(
    """
    SELECT 
        {} 
    FROM 
        {} AS {}
        {} JOIN 
        {} AS {}
        ON {} = {}
    """
)
SELECT_FROM_JOINED_TABLES_WITH_FILTER_TEMPLATE = SQL(
    """
    SELECT 
        {} 
    FROM 
        {} AS {}
        {} JOIN 
        {} AS {}
        ON {} = {}
    WHERE {} = %s
    """
)

ALLOWED_JOIN_TYPES = {
    'INNER',
    'LEFT',
    'RIGHT',
    'FULL',
}

def make_column_names_string(columns: list[str] | None = None) -> psycopg2.sql.SQL | psycopg2.sql.Composed:
    """
    Helper function for making selected column string for a SQL query

    :param columns: list[str] | None, list of columns to be selected via the query or None if all to be selected
    :return: psycopg2.sql.SQL | psycopg2.sql.Composed, returns SQL when no columns were passed and Composed otherwise
    """
    # If no columns were passed then all will be returned
    if not columns:
        return SQL('*')

    # If more than one was passed then join them by ', '
    return  SQL(', ').join( Identifier(col) for col in columns )

def get_records(
        connection: psycopg2.extensions.connection,
        table_name: str,
        filter_column: str | None = None,
        filter_value: str | None = None,
        columns: list[str] | None = None,
) -> tuple:
    """
    Retrieves records from a given table in the database by filter_value

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param table_name: str, unique identifier used for a table name
    :param filter_column: str | None, table grouping (values: 'works', 'authors', 'editions')
    :param filter_value: str | None, unique identifier used to filter records
    :param columns: list[str] | None, list of field names to be retuned for the records or
                                      None if all columns to be returned

    :returns: tuple, containing query results and column names
    """

    # Make column names string
    selected_column_names = make_column_names_string(columns)

    # Query the database
    with connection.cursor() as cursor:

        # If no filter column or no filter_value was given then fetch records without filtering
        if filter_column is None or filter_value is None:

            # Setting up the template for the query
            query_template = SELECT_FROM_TABLE_TEMPLATE

            # Setting up the queries formatting arguments
            # (i.e. column names. table name)
            formatting_args = (
                selected_column_names,
                Identifier(table_name)
            )

            # Setting up the queries variables
            # (i.e. filtering value)
            query_variables = None

        else:
            # Setting up the template for the query
            query_template = SELECT_FROM_TABLE_WITH_FILTER_TEMPLATE

            # Setting up the queries formatting arguments
            # (i.e. column names. table name)
            formatting_args = (
                selected_column_names,
                Identifier(table_name),
                Identifier(filter_column)
            )

            # Setting up the queries variables
            # (i.e. filtering value)
            query_variables =  (filter_value,)

        # Construct the query
        query = query_template.format(*formatting_args)

        # Execute the query
        cursor.execute(query, query_variables)

        # Fetch all records as returned
        records = cursor.fetchall()

        # Fetch column names as returned
        column_names = get_column_names(cursor)

        return records, column_names

def get_records_by_join(
        connection: psycopg2.extensions.connection,
        left_table: str,
        left_alias:str,
        right_table: str,
        right_alias: str,
        join_type: str,
        left_key: str,
        right_key:str,
        filter_column: str | None = None,
        filter_value: str | None = None,
        columns: list[str] | None = None,
) -> tuple:
    """
    Retrieves records from a joining two tables in the database with row filtering

    :param connection: psycopg2.extensions.connection, active PostgreSQL database connection
    :param left_table: str, name of the left table in the join
    :param left_alias: str, alias assigned to the left table
    :param right_table: str, name of the right table in the join
    :param right_alias: str, alias assigned to the right table
    :param join_type: str, SQL join type (e.g. 'INNER', 'LEFT', 'RIGHT', 'FULL')
    :param left_key: str, join column from the left table
    :param right_key: str, join column from the right table
    :param filter_column: str | None, column used in the WHERE clause
    :param filter_value: str | None, value used to filter records
    :param columns: list of columns to select or None if all columns are to be returned
    :type columns: list[str] | None, list of field names to be retuned for the records or
                                      None if all columns to be returned

    :returns: tuple, containing query results and column names
    """

    if join_type.upper() not in ALLOWED_JOIN_TYPES:
        raise ValueError(f'Unsupported join type \'{join_type}\'')

    # Make column names string
    selected_column_names = make_column_names_string(columns)

    # Query the database
    with connection.cursor() as cursor:

        # If no filter column or no filter_value was given then fetch records without filtering
        if filter_column is None or filter_value is None:

            # Setting up the template for the query
            query_template = SELECT_FROM_JOINED_TABLES_WITHOUT_FILTER_TEMPLATE

            # Setting up the queries formatting arguments
            # (i.e. column names. table name)
            formatting_args = (
                selected_column_names,
                Identifier(left_table),
                Identifier(left_alias),
                SQL(join_type.upper()),
                Identifier(right_table),
                Identifier(right_alias),
                Identifier(left_alias, left_key),
                Identifier(right_alias, right_key),
            )

            # Setting up the queries variables
            # (i.e. filtering value)
            query_variables = None

        else:
            # Setting up the template for the query
            query_template = SELECT_FROM_JOINED_TABLES_WITH_FILTER_TEMPLATE

            # Setting up the queries formatting arguments
            # (i.e. column names. table name)
            formatting_args = (
                selected_column_names,
                Identifier(left_table),
                Identifier(left_alias),
                SQL(join_type.upper()),
                Identifier(right_table),
                Identifier(right_alias),
                Identifier(left_alias, left_key),
                Identifier(right_alias, right_key),
                Identifier(left_alias, filter_column)
            )

            # Setting up the queries variables
            # (i.e. filtering value)
            query_variables =  (filter_value,)

        # Construct the query
        query = query_template.format(*formatting_args)

        # Execute the query
        cursor.execute(query, query_variables)

        # Fetch all records as returned
        records = cursor.fetchall()

        # Fetch column names as returned
        column_names = get_column_names(cursor)

        return records, column_names
