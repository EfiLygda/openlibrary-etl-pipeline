import re
import pandas as pd
import numpy as np

def find_year(date: str) -> int | float:
    """
    Export the year from a date string using a regex
    :param date: str, the date string
    :return: int | float, the year or np.nan if it is not available
    """

    # The regex pattern to extract a year from a string
    year_pattern = r'\d{4}'

    # If the date is a string the year is extracted
    if isinstance(date, str):

        # Find all year matches
        matches = re.findall(year_pattern, date)

        # If any match is found then the first is returned, else if there are more np.nan is returned
        if matches:

            # Check how many matches were found
            if len(matches) == 1:
                return int(matches[0])
            else:
                # raise ValueError(f'In \'{date}\' more than one year were found: \'{matches}\'')
                return np.nan

        # If no match is found then np.nan is returned
        else:
            return np.nan

    # If date is not a string then np.nan is returned
    else:
        return np.nan

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
        if not is_primary_key(df[primary_key]):
            raise ValueError(f'\'{primary_key}\' is not primary key for \'{table_name}\' table.')
        else:
            print(f'\'{table_name}\' Primary Key: \'{primary_key}\'')

    # Cast the new data types, if given
    if dtypes:
        df = df.astype(dtypes)

    return df

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
        table_name: str
) -> None:
    """
    Helper function for printing a message of whether to explode or not a column depending on if it has
    at least one multivalue list or not
    :param col: pd.Series, the column to use for the check
    :param table_name: str, name of the table
    :return: None
    """
    if any_multivalue_list(col):
        print(
            f'Column \'{col.name}\' of table \'{table_name}\' has at least one multivalue list -> explode \'{col.name}\''
        )
    else:
        print(
            f'Column \'{col.name}\' of table \'{table_name}\' does not have multivalue lists -> do not explode \'{col.name}\''
        )

def get_language(value: str) -> str:
    """
    Function for extracting the language name from strings like '/languages/{language}'
    :param value: str, the string from which the language name is extracted
    :return: str, the extracted language name
    """
    return value.strip().replace('/languages/', '')

def extract_text(x: dict) -> str | float:
    """
    Function for extracting the text from rows with text as dictionary
    :param x: dict, the dictionary with the text
    :return: str | float: the string with the text or np.nan if it is missing
    """
    if isinstance(x, dict) and 'value' in x.keys():
        return x['value']
    elif isinstance(x, str):
        return x
    else:
        return np.nan
