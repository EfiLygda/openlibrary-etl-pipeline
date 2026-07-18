"""
STEP 3: Use OpenLibraryClient.get_many to extract via keys all WORKS_ENRICHED, AUTHORS, SERIES

DETAILS:
1. WORKS_ENRICHED contains enriched data not returned from SEARCH in STEP 1
2. The queries used for each object is:
    2.1 WORKS_ENRICHED: WORKS @ etl/extract/docs/entrypoints.md
    2.2 AUTHORS:        AUTHORS @ etl/extract/docs/entrypoints.md
    2.3 SERIES:         SERIES @ etl/extract/docs/entrypoints.md
3. The results are saved as JSON files @ :
    3.1 WORKS_ENRICHED: data/raw/romance_fiction/works_enriched
    3.2 AUTHORS:        data/raw/romance_fiction/authors
    3.3 SERIES:         data/raw/romance_fiction/series
"""
import os
import re

from data_pipeline import open_library

from config.paths import KEYS_DIR, WORKS_DIR, AUTHORS_DIR, SERIES_DIR
from config.openlibrary_api import MAX_ATTEMPTS

from utilities.io import load_json, save_json
from utilities.rate_limit import wait
from data_pipeline.utils.data.batching import make_batches
from data_pipeline.utils.retry import retry
from utilities.logging import set_logger, log_result

logger = set_logger('FETCH_WORKS_AUTHORS_SERIES')

@retry(logger, failure_msg='ATTEMPT_FAILED')
def fetch_records_batch(
        client: open_library.Client,
        key_batch: list[str]
) -> dict:
    """
    Fetch a batch of records from the OpenLibrary API.

    This operation is wrapped with a retry decorator that automatically
    handles API failures (timeouts, connection errors, HTTP errors)
    and retries the request before failing.

    :param client: open_library.Client, OpenLibrary API client
    :param key_batch: list[str], list of record keys to fetch in a single request

    :return: dict, API response containing fetched records

    :raises ValueError: if the API returns no results for the requested batch
    """
    # Querying the API for the current batch
    records = client.get_many(key_batch)

    # If no records are returned a ValueError is returned
    if not records['result']:
        raise ValueError(f'No results were returned from {client.last_url}')

    return records


def run():

    logger.info('STAGE_START')

    # Setting up thw Open Library client for querying the API
    client = open_library.Client()

    # The regex used for later extracting the type of keys in the JSON
    # keys files extracted from export_keys.py
    key_type_pattern = r'.+_(work|author|series)_.+\.json$'

    # Connecting the type of keys with their respective saved directories
    dirs = {
        'work': WORKS_DIR,
        'author': AUTHORS_DIR,
        'series': SERIES_DIR
    }

    # For each key file the API will be queried in batches using as batch size
    # client.LIMIT and the results will be saved in JSON files
    for key_file_name in os.listdir(KEYS_DIR):

        # The file path of the current key file
        key_file_path = os.path.join(KEYS_DIR, key_file_name)

        # Finding if there is the key type in the name of the file
        key_type_match = re.search(key_type_pattern, key_file_name)

        # If a match is not made a ValueError is raised
        if not key_type_match:
            logger.warning(f'KEY_TYPE_PARSE_FAILED filename={key_file_name} expected_types=work,author,series')
            continue

        # Extracting the key type from the file name
        key_file_type = key_type_match.group(1)

        # Loading the current key list
        keys_list = load_json(key_file_path)

        # Setting the batch size for querying
        batch_size = client.LIMIT

        # Creating the batches from the key list
        key_batches = make_batches(keys_list, batch_size)

        # For each batch the API is queried and the results are saved
        for i, key_batch in enumerate(key_batches):

            # The file name for the current batch
            batch_filename = f'{key_file_type.upper()}_p{i+1}.json'

            # Finding the current key type directory to save the records
            key_type_dir = dirs[key_file_type]

            # The file path for the current batch
            batch_filepath = os.path.join(key_type_dir, batch_filename)

            # Fetch current batch's records with built-in retries in case of errors
            records = fetch_records_batch(client, key_batch)

            # Add final 's' to entrypoint name in case it doesn't exist
            # (expected values: author, work, series)
            entrypoint_name = key_file_type + 's' if not key_file_type.endswith('s') else key_file_type

            # Add enriched suffix to works
            # if 'work' in entrypoint_name.lower():
            #     entrypoint_name += '_enriched'

            # Log messages to be used
            success_msg = (
                f'{entrypoint_name.upper()}_GET_MANY_SUCCESS batch={i + 1}/{len(key_batches)} '
                f'file={batch_filename} '
                f'attempt={records['attempts']}/{MAX_ATTEMPTS} '
                f'duration={records['duration']:.2f}s'
            )

            error_msg = (
                f'{entrypoint_name.upper()}_GET_MANY_FAILED batch={i + 1}/{len(key_batches)} '
                f'error_type={records['error']} '
                f'file={batch_filename} '
                f'attempt={records['attempts']}/{MAX_ATTEMPTS} '
                f'duration={records['duration']:.2f}s'
            )

            # Success flag
            is_successful = records['success']

            # Log the result using the proper message and level
            log_result(
                logger=logger,
                is_successful=is_successful,
                success_msg=success_msg,
                error_msg=error_msg
            )

            # Continue to next batch if no data is available
            if not is_successful:
                continue

            # Saving the current batch
            save_json(records['results'], batch_filepath)

            wait()

    logger.info('STAGE_COMPLETE')
