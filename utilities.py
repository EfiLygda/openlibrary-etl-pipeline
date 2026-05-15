import re
import pandas as pd
import numpy as np
from time import sleep
from random import uniform


def wait(seconds: float = 3) -> None:
    """
    Function for politely waiting more than 3 seconds for each request
    :param seconds: float, the minimum seconds to wait
    :return: None
    """
    sleep(seconds + uniform(0, 1.5))

def make_batches(lst: list[str], batch_size: int) -> list[list[str]]:
    """
    Make batches from list using a predetermined batch size
    :param lst: list, the list to make batches from
    :param batch_size: int, the batch size for the batches
    :return: list[list[str]], the list containing the batches as lists of strings
    """

    batches = [
        lst[i: i + batch_size]
        for i in range(0, len(lst), batch_size)
    ]

    return  batches

def sep() -> None:
    """
    Function for printing a line seperator
    :return: None
    """
    print(100 * '-')

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

def prepare_table(
        df: pd.DataFrame,
        dtypes: dict = None,
        primary_key: str | list[str] = None,
        table_name: str = ''
) -> pd.DataFrame:
    """
    Prepare tables:
    1. Strip string columns
    2. Check if the suggested primary key is indeed a primary key (unique value and no NaN)
    3. Recast dtypes as given

    :param df: pandas.DataFrame, the dataframe to prepare
    :param dtypes: dict | None, dictionary with the column names and their new data types
    :param primary_key: str, name of the suggested column to be used a primary key
    :param table_name: str, the name of the table
    :return: pandas.DataFrame, the dataframe prepared
    """

    # Strip string columns
    df = strip_columns(df)

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
