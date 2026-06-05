"""
Request throttling utility.

Provides a helper function for introducing randomized delays
to simulate polite API request pacing and reduce rate limiting.
"""

from time import sleep
from random import uniform

def wait(seconds: float = 1) -> None:
    """
    Function for politely waiting more than 1 seconds for each request
    :param seconds: float, the minimum seconds to wait
    :return: None
    """
    sleep(seconds + uniform(0, 1.5))