"""
Validation and integrity-check utilities for ETL processing.

Provides helper functions for:
- Detecting missing values and uniqueness
- Validating primary keys
- Handling multi-value fields
- Checking database table existence
"""

import numpy as np
import pandas as pd

import psycopg2
from logging import Logger, LoggerAdapter

def has_na(values: pd.Series | pd.DataFrame) -> np.bool | None:
    """
    Check if a column or dataframe has at least one missing value
    :param values: pd.Series | pd.DataFrame, a column or dataframe to check for missing values
    :return: np.bool | None, returns np.True_ or np.False_ for missing values or None if 'values' is not
                              pd.Series | pd.DataFrame
    """
    if isinstance(values, pd.Series):
        # Check if there is at least a missing value in the column
        return values.isna().any()
    elif isinstance(values, pd.DataFrame):
        # Check if there is at least a missing value in the columns (first .any()) and then
        # if any column had at least a missing value (second .any())
        return values.isna().any().any()
    else:
        # Return None if 'values' is not pd.Series | pd.DataFrame
        return None

def is_unique(values: pd.Series | pd.DataFrame) -> np.bool | None:
    """
    Check if a column or dataframe has unique values
    :param values: pd.Series | pd.DataFrame, a column or dataframe to check for unique values
    :return: np.bool | None, returns np.True_ or np.False_ for unique values or None if 'values' is not
                              pd.Series | pd.DataFrame
    """
    if isinstance(values, pd.Series):
        # Check if all values are unique for the column
        return values.is_unique
    elif isinstance(values, pd.DataFrame):
        # Check if the count of values is the same before and after dropping duplicates from the dataframe
        return len(values) == len(values.drop_duplicates())
    else:
        # Return None if 'values' is not pd.Series | pd.DataFrame
        return None

def is_primary_key(values: pd.Series | pd.DataFrame) -> bool:
    """
    Check if a single column (or more) is a primary key (unique values and no missing values)
    :param values: pd.Series | pd.DataFrame, a column or dataframe to check it can be used a primary key
    :return: bool, True if it can be used or False if it cannot
    """
    # Check if the values are unique and have no missing values
    if not has_na(values) and is_unique(values):
        return True
    else:
        return False

def any_multivalue_list(col: pd.Series) -> np.bool:
    """
    Function that detects whether a column has at least one list that has more than one value
    :param col: pd.Series, the column to be used
    :return: np.bool, np.True_ if column has at least one list that has more than one value,
                      np.True_ if not
    """
    return (col.dropna().apply(len) != 1).any()

def check_explode(
        col: pd.Series,
        table_name: str,
        logger: Logger | LoggerAdapter[Logger] | None = None
) -> None:
    """
    Helper function for printing a message of whether to explode or not a column depending on if it has
    at least one multivalue list or not
    :param col: pd.Series, the column to use for the check
    :param table_name: str, name of the table
    :param logger: Logger | LoggerAdapter[Logger] | None, the logger used
    :return: None
    """

    # The messages used in case there is a need or not to explode a column
    # explode_msg = f'Column \'{col.name}\' of table \'{table_name}\' has at least one multivalue list -> explode \'{col.name}\''
    # do_not_explode_msg = f'Column \'{col.name}\' of table \'{table_name}\' does not have multivalue lists -> do not explode \'{col.name}\''
    explode_msg = (
        f'COLUMN_EXPLODE_DECISION '
        f'column={col.name} '
        f'table={table_name} '
        f'action=explode '
        f'reason=multivalue_detected'
    )

    do_not_explode_msg = (
        f'COLUMN_EXPLODE_DECISION '
        f'column={col.name} '
        f'table={table_name} '
        f'action=do_not_explode '
        f'reason=single_value_per_row'
    )

    # Find the right message to be displayed
    if any_multivalue_list(col):
        message = explode_msg
    else:
        message = do_not_explode_msg

    # Check if a logger is used or else print the message
    if logger:
        logger.info(message)
    else:
        print(message)

def check_if_table_exists(
        cursor: psycopg2.extensions.cursor,
        table_name: str,
        schema: str = 'public',
        logger: Logger | LoggerAdapter[Logger] | None = None
) -> bool:
    """
    Function for validating if a table exists in a schema
    :param cursor: psycopg2.extensions.cursor, cursor object for the current database
    :param table_name: str, the name of the table
    :param schema: str, the name of the schema to check
    :param logger: Logger | LoggerAdapter[Logger] | None, the logger to be used
    :return: bool
    """

    query = """
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.tables
            WHERE table_schema = %s
              AND table_name = %s
        );
    """

    cursor.execute(query, (schema, table_name))

    table_exists = cursor.fetchone()[0]

    exists_msg = f'TABLE_EXISTS table={table_name}'
    not_exists_msg = f'TABLE_CREATE_REQUIRED table={table_name}'

    if table_exists:
        message = exists_msg
    else:
        message = not_exists_msg

    if logger:
        logger.warning(message)
    else:
        print(message)

    return table_exists

def check_if_index_exists(
        cursor: psycopg2.extensions.cursor,
        index_name: str,
        logger: Logger | LoggerAdapter[Logger] | None = None
) -> bool:
    """
    Function for validating if an index exists in a schema
    :param cursor: psycopg2.extensions.cursor, cursor object for the current database
    :param index_name: str, the name of the table
    :param schema: str, the name of the schema to check
    :param logger: Logger | LoggerAdapter[Logger] | None, the logger to be used
    :return: bool
    """

    query = """
        SELECT EXISTS (
            SELECT  1
            FROM    pg_indexes
            WHERE   indexname = %s
        );  
    """

    cursor.execute(query, (index_name,))

    index_exists = cursor.fetchone()[0]

    exists_msg = f'INDEX_EXISTS table={index_name}'
    not_exists_msg = f'INDEX_CREATE_REQUIRED table={index_name}'

    if index_exists:
        message = exists_msg
    else:
        message = not_exists_msg

    if logger:
        logger.warning(message)
    else:
        print(message)

    return index_exists