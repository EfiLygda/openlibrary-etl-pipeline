import re
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