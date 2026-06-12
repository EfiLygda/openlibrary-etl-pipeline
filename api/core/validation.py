"""
Basic validation helper function for records
"""

import numpy as np

def duplicate_column_names(column_names: list[str]) -> np.ndarray[str]:
    """
    Returns array with the duplicate column names

    :param column_names: list[str], list with column names

    :return: np.ndarray[str], array with the duplicate column names
    """

    # Find the unique fields/columns and their number of appearances in the fields argument
    unique_column_names, unique_column_names_counts = np.unique(column_names, return_counts=True)

    # Return only duplicate fields
    return unique_column_names[unique_column_names_counts > 1]

def all_rows_have_identical_values_in_duplicate_columns(
        records: list,
        column_names: list[str]
) -> np.bool_:
    """
    Whether columns with duplicate column names have the same values across all their rows

    :param records: list, list of records
    :param column_names: list[str], column names for the records

    :return:
    """

    # Find duplicate column names
    duplicate_fields = duplicate_column_names(column_names)

    # If no duplicate column names were found return False
    if duplicate_fields.size == 0:
        return np.True_

    # Mask for duplicate column names
    duplicate_column_name_mask = np.isin(column_names, duplicate_fields)

    # Convert records to arrays
    records = np.array(records)

    # Fetch only duplicat column names columns
    duplicate_columns = records[:, duplicate_column_name_mask]

    # Check and return whether every row for these columns has the same values
    return np.all(
        duplicate_columns == duplicate_columns[:,[0]]
    )