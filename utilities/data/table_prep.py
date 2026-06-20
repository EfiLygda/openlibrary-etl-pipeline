"""
DataFrame cleaning and preparation utilities.

Provides functions for:
- String cleanup and normalization
- Row filtering based on missing values
- Primary key validation
- Table preprocessing pipeline with optional dtype casting
"""

import pandas as pd
from logging import Logger, LoggerAdapter
from .validation import is_primary_key

def strip_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Strip string values from string columns
    :param df: pandas.DataFrame, the dataframe from which every string value is stripped
    :return: pandas.DataFrame, the dataframe with every string value stripped
    """

    # For each column check if it is 'string' data type and strip every value
    for col_name in df.columns:
        if df[col_name].dtype == 'string':
            df[col_name] = df[col_name].str.strip()

    return df

def drop_rows_with_only_pk(
        df: pd.DataFrame,
        primary_key: str | list[str]
) -> pd.DataFrame:
    """
    Function for removing rows where all fields are none except rhe primary key
    :param df: pd.DataFrame, the dataframe to be used
    :param primary_key: str | list[str], the name or names of the column/s to be used as primary key
    :return: pd.DataFrame, the dataframe after removing rows where all fields are none except rhe primary key
    """

    # Convert column names to list
    column_names = list(df.columns)

    # If primary key is multivalue then remove each column name from the list
    # else just remove the primary key name from the columns
    if isinstance(primary_key, list):
        for col_name in primary_key:
            column_names.remove(col_name)
    else:
        column_names.remove(primary_key)

    # Remove rows where all columns have missing values except of the primary key
    df = df.dropna(subset=column_names, how='all')

    return df

def prepare_table(
        df: pd.DataFrame,
        dtypes: dict = None,
        primary_key: str | list[str] = None,
        table_name: str = '',
        drop_na_except: str | list[str] = None,
        drop_duplicates: bool = True,
        logger: Logger | LoggerAdapter[Logger] | None = None
) -> pd.DataFrame:
    """
    Prepare tables pipeline:
    1. Strip string columns
    2. Drop duplicate rows
    3. Remove rows where, except the primary key, all the other fields have missing values
    4. Check if the suggested primary key is indeed a primary key (unique values and no missing values)
    5. Recast dtypes as given

    :param df: pandas.DataFrame, the dataframe to prepare
    :param dtypes: dict | None, dictionary with the column names and their new data types
    :param primary_key: str, name of the suggested column to be used a primary key
    :param table_name: str, the name of the table
    :param drop_duplicates: bool, True if to drop duplicates, False if not to
    :param drop_na_except: str, the name of the column to exclude when searching for rows with all missing rows
    :param logger: Logger | LoggerAdapter[Logger] | None, the logger to be used
    :return: pandas.DataFrame, the dataframe prepared
    """

    # Strip string columns
    df = strip_columns(df)

    # Drop duplicate rows
    if drop_duplicates:
        df = df.drop_duplicates()

    # Drop rows where, except the selected column, all the other fields have missing value
    if drop_na_except:
        df = drop_rows_with_only_pk(df, drop_na_except)

    # Check if  suggested column can be used as a primary key
    if primary_key:
        if logger:
            if not is_primary_key(df[primary_key]):
                logger.error(
                    f'PRIMARY_KEY_VALIDATION_FAILED '
                    f'table={table_name} '
                    f'primary_key={primary_key}'
                )
            else:
                logger.info(
                    f'PRIMARY_KEY_VALIDATION_SUCCESS '
                    f'table={table_name} '
                    f'primary_key={primary_key}'
                )
        else:
            if not is_primary_key(df[primary_key]):
                raise ValueError(f'\'{primary_key}\' is not primary key for \'{table_name}\' table.')
            else:
                print(f'\'{table_name}\' primary key is \'{primary_key}\'')

    # Cast the new data types, if given
    if dtypes:
        df = df.astype(dtypes)

    return df
