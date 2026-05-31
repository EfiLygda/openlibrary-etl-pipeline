"""
CSV input/output utilities.
"""

import os
import pandas as pd

def read_csv(filepath: str) -> pd.DataFrame:
    """
    Wrapper function for reading CSV files via pandas
    :param filepath: str, the tables file path
    :return: pd.DataFrame, the table as a pandas dataframe
    """
    return pd.read_csv(filepath)

def save_csv(df: pd.DataFrame, filename: str, directory: str) -> None:
    """
    Function for exporting a table as a CSV file without also exporting its index
    :param df: pd.DataFrame, the table to be exporting
    :param filename: str, the filename
    :param directory: str, the directory in which the file will be exported to
    :return: None
    """
    df.to_csv(
        os.path.join(directory, filename),
        index=False,
    )
