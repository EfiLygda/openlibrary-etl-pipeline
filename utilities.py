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

def sep():
    print(100 * '-')

def find_year(date: str) -> int | float:
    """
    Export the year from a date string using a regex
    :param date: str, the date string
    :return: int | float, the year or np.nan if it is not available
    """
    year_pattern = r'\d{4}'

    if isinstance(date, str):

        matches = re.findall(year_pattern, date)

        if matches:
            return int(matches[0])
        else:
            return np.nan
    else:
        return np.nan

def strip_columns(df: pd.DataFrame) -> pd.DataFrame:

    for col_name in df.columns:
        if df[col_name].dtype == 'string':
            df[col_name] = df[col_name].str.strip()

    return df

def has_na(values: pd.Series | pd.DataFrame) -> np.bool | None:
    if isinstance(values, pd.Series):
        return values.isna().any()
    elif isinstance(values, pd.DataFrame):
        return values.isna().any().any()
    else:
        return None

def is_unique(values: pd.Series | pd.DataFrame) -> np.bool | None:
    if isinstance(values, pd.Series):
        return values.is_unique
    elif isinstance(values, pd.DataFrame):
        return len(values) == len(values.drop_duplicates())
    else:
        return None

def is_primary_key(values: pd.Series | pd.DataFrame) -> bool:
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
