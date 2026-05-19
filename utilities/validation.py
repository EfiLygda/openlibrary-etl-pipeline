import pandas as pd
import numpy as np

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