import logging
from logging import Logger, LoggerAdapter

LOGGING_FORMAT = '%(asctime)s | [%(levelname)s] | %(filename)s | [%(stage)s] %(message)s'
DATE_FORMAT = '%m/%d/%Y %I:%M:%S %p'

def sep() -> None:
    """
    Function for printing a line seperator
    :return: None
    """
    print(100 * '-')

class SafeFormatter(logging.Formatter):
    """
    Class inheriting from logging.Formatter in order to handle different LogRecord's formatting
    Notes: 1. Basically provides wrapper around logging.Formatter.format for handling new formatting
              variable `stage` when not available in a given logging.LogRecord
           2. Some logs, especially with DEBUG do not include this variable, so there were errors when used
    """
    def format(self, record: logging.LogRecord) -> str:
        """
        Wrapper function around logging.Formatter.format for handling new formatting
        variable `stage` when not available in the logging.LogRecord
        :param record: logging.LogRecord, the original LogRecord to add new variable `stage`
        :return: str, the converted log text with added new variable `stage` when not available
                      in the logging.LogRecord
        """
        # Use a default value if missing 'stage' variable from Log Record
        if not hasattr(record, "stage"):
            record.stage = "-"

        # Return the formatted LogRecord using the original logging.Formatter.format
        return super().format(record)

def config_logger(filepath: str | None = None, level='debug') -> None:
    """
    Function for configuring all loggers.
    Configurations:
    1.
    :param filepath: str | None, the filepath for the log file to be exported, if given
    :param level: str, the logging level (Options: 'debug', 'info', 'warning', 'error', 'critical')
    :return: None
    """

    # Setting up the log levels to be used via 'level' argument
    log_levels = {
        'DEBUG': logging.DEBUG, # change to logging.DEBUG to see everything
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    # Check if level is invalid and raise ValueError else
    level = level.upper()
    if level not in log_levels.keys():
        raise ValueError(f"Invalid log level: {level}")

    # Setting up file handler if 'filename' is available
    handlers = []

    if filepath:

        # Setting up a logging file handler for given 'filename'
        file_handler = logging.FileHandler(
            filepath,
            mode='w',
            encoding="utf-8"
        )

        # Set up the safe formatting in case in a log record 'stage' is not available
        formatter = SafeFormatter(
            LOGGING_FORMAT,
            datefmt=DATE_FORMAT
        )

        # Add to it the safe formatting
        file_handler.setFormatter(formatter)

        # Add the file handler to handlers list
        handlers.append(file_handler)

    # Set up the safe formatting in case in a log record 'stage' is not available
    formatter = SafeFormatter(
        LOGGING_FORMAT,
        datefmt=DATE_FORMAT
    )

    # Set up stream handler
    stream_handler = logging.StreamHandler()

    # Add to it the safe formatting
    stream_handler.setFormatter(formatter)

    # Add the stream handler to handlers list
    handlers.append(stream_handler)

    # Configuring the logging
    logging.basicConfig(
        level=log_levels[level],
        handlers=handlers,
        # force=True
    )

def set_logger(stage: str | None = None) -> Logger | LoggerAdapter[Logger]:
    """
    Function for setting up a logger
    :param stage: str | None, the name of stage for the logger
    :return: Logger | LoggerAdapter[Logger], the logger
    """
    # Set up the logger
    logger = logging.getLogger(__name__)

    # The logger with contextual information, namely the 'stage'
    # Note: Some logs, especially with DEBUG do not include this variable, so there were errors when used
    if stage:
        logger = logging.LoggerAdapter(logger, {"stage": stage})

    return logger