import os
import pandas as pd

def read_csv():
    pass

def save_csv(df: pd.DataFrame, filename: str, directory: str) -> None:
    """
    Function for exporting a table as a CSV file without also exporting its index
    :param df: pd.DataFrame, the table to be exporting
    :param filename: str, the filename
    :param directory: str, the directory in which the file will exported to
    :return: None
    """
    df.to_csv(
        os.path.join(directory, filename),
        index=False,
    )
