"""
Data parsing and extraction utilities.

Provides helper functions for extracting structured values from raw
Open Library API responses, including dates, languages, and nested text fields.
"""

import re
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