"""
Retry utility decorator for robust API data extraction.

This module provides a reusable decorator factory that adds retry logic
to functions performing external API calls or other unreliable operations.

The retry mechanism:
- Retries a function up to MAX_ATTEMPTS times
- Handles common network-related exceptions (timeouts, connection errors, HTTP errors)
- Logs each failed attempt using a provided logger
- Waits between retries using a configurable delay function

Instead of returning the raw function output, the decorated function
returns a structured dictionary containing:
- attempts: number of attempts used
- success: whether the operation succeeded
- results: function output (if successful)
- duration: duration of operation
- error: error message (if failed)


DETAILS: Explanation for type hinting

1. `F = TypeVar("F", bound=Callable[..., Any])`

    Type variable representing any callable function with any signature and return type
--------------------------------------------------------------------------------------------------
2. `wrapper(*args, **kwargs) -> dict`

    Wrapper function around `func`

    ARGUMENTS: ANY
    RETURNS: dictionary like
    {
        'attempts': attempt,
        'success': True,
        'results': func(*args, **kwargs), # Or None
        'error': None # Or Exception
    }
--------------------------------------------------------------------------------------------------
3. `decorator(func: F) ->  Callable[..., dict]`

    Decorator (function)

    ARGUMENTS: F (any callable function with any signature and return type)
    RETURNS: wrapper (callable function with any arguments and return type dictionary)
--------------------------------------------------------------------------------------------------
4. retry(
        logger: Logger | LoggerAdapter[Logger],
        failure_msg: str = ''
    ) -> Callable[[F], Callable[..., dict]]

    Decorator factory for retrials

    ARGUMENTS:
        1. logger: Logger | LoggerAdapter[Logger],
        2. failure_msg: str = ''

    RETURNS:
        decorator (callable function with argument F (any callable function with
        any signature and return type) and return type wrapper (callable function with any
        arguments and return type dictionary)
"""

from time import time
import requests
from typing import Callable, Any, TypeVar
from logging import Logger, LoggerAdapter
from config.api import MAX_ATTEMPTS
from utilities.rate_limit import wait

# Type variable representing any callable function with any signature and return type
F = TypeVar("F", bound=Callable[..., Any])

# The exceptions to be caught in the decoratory for retrying to fetch data
DEFAULT_EXCEPTIONS = (
    requests.exceptions.ReadTimeout,  # connection error
    requests.exceptions.ConnectTimeout,  # connection error
    requests.exceptions.HTTPError,  # no data available
    requests.exceptions.ConnectionError,  # connection error
    ValueError, # no data
)

# Classification of expected exceptions
EXCEPTION_MAP = {
    requests.exceptions.ReadTimeout: 'read_timeout',
    requests.exceptions.ConnectTimeout: 'connect_timeout',
    requests.exceptions.HTTPError: 'http_error',
    requests.exceptions.ConnectionError: 'connection_error',
    ValueError: 'no_data'
}

def classify_exception(exception: Exception) -> str:
    """

    """
    for exc_type, label in EXCEPTION_MAP.items():
        if isinstance(exception, exc_type):
            return label

    return "unknown_error"

def retry(
        logger: Logger | LoggerAdapter[Logger],
        failure_msg: str = ''
) -> Callable[[F], Callable[..., dict]]:
    """
    Decorator factory that adds retry logic to a function.

    The decorated function will be automatically retried up to MAX_ATTEMPTS
    times if it raises transient API-related exceptions.

    Each execution returns a structured dictionary containing:
        - number of attempts used
        - success status
        - function result (if successful)
        - duration of operation
        - error message (if failed)

    :param logger: Logger | LoggerAdapter[Logger], the logger used for logging,
    :param failure_msg: str, base message in case of error during the attempts
    :return: Callable[..., Any], a function that can take any arguments and returns anything
    """

    def decorator(func: F) ->  Callable[..., dict]:
        """
        Wraps a function with retry logic.

        The original function signature is preserved for inputs,
        but the return type is transformed into a structured dictionary.

        :param func: Function to be wrapped with retry logic
        :return: Wrapper function returning a retry result dictionary
        """

        def wrapper(*args, **kwargs) -> dict:
            """
            Executes the wrapped function with retry behavior.

            On success:
                returns a dictionary with success=True and the function result.

            On failure:
                retries up to MAX_ATTEMPTS and returns success=False with error info.

            :param args: Positional arguments passed to the original function
            :param kwargs: Keyword arguments passed to the original function
            :return: Dictionary containing execution metadata and result
            """

            # Set up start time of operation
            start_time = time()

            # Set up exception
            last_exception = None

            for attempt in range(1, MAX_ATTEMPTS+1):

                try:

                    # Fetch the results
                    results = func(*args, **kwargs)

                    # Calculate duration of operation, in case of success
                    duration = time() - start_time

                    return {
                        'attempts': attempt,
                        'success': True,
                        'results': results,
                        'duration': duration,
                        'error': None
                    }

                except DEFAULT_EXCEPTIONS as e:

                    # keep last exception
                    last_exception = e

                    # Classify the error
                    error_type = classify_exception(last_exception)

                    # In case of an error log a debug message
                    logger.debug(f'{failure_msg} attempt={attempt} error_type={error_type}')

                    # Politely wait more than 1 seconds and try again
                    wait()

            # Calculate duration of operation, in case of failure
            duration = time() - start_time

            return {
                'attempts': MAX_ATTEMPTS,
                'success': False,
                'results': None,
                'duration': duration,
                'error': error_type if last_exception else None
            }

        return wrapper

    return decorator



