"""
STEP 4: Export author key and name pairs.

DETAILS:
1. Data are saved in a JSON file @ data/keys
2. Some records that were returned from STEP 1 were redirecting to another records.
   In such cases OpenLibraryClient.get_redirected_record is used to find the right record and
   the final data were added to the final data. As such no data is lost.
"""
import os

import open_library

from config.paths import AUTHORS_DIR, KEYS_DIR
from config.api import GENRE_facet, MAX_ATTEMPTS

from utilities.io import load_json, save_json
from utilities.retry import retry
from utilities.logging import set_logger, log_result

logger = set_logger('EXPORT_AUTHOR_KEY_NAMES')

@retry(logger, failure_msg='ATTEMPT_FAILED')
def fetch_redirected_record(
        client: open_library.Client,
        record: dict,
        original_key: str,
        filepath: str
) -> dict:
    """
    Fetch a redirected record from the OpenLibrary API and export it.

    This operation is wrapped with a retry decorator that automatically
    handles API failures (timeouts, connection errors, HTTP errors)
    and retries the request before failing.

    Some OpenLibrary records act as redirects to a canonical record.
    This function resolves such redirects and returns the final record.

    :param client: open_library.Client, OpenLibrary API client
    :param record: dict, original record which may contain a redirect reference
    :param original_key: str, original record's key for logging purposes
    :param filepath: str, destination path for record

    :return: dict, the redirected record
    """

    # Fetch the record that the original redirects to
    redirect_key, record = client.get_redirected_record(record)

    # Export it to the right format
    record_to_export = {'result': {record['key']: record}}
    save_json(record_to_export, filepath)

    # Log the redirection
    logger.info(
        f'Key \'{original_key}\' redirects to \'{record['key']}\' -> added new raw page but original stays as is'
    )

    return record


def run():
    logger.info(f'Starting exporting of all authors\' keys and names')

    # Setting up thw Open Library client for querying the API
    client = open_library.Client()

    # Setting up the dictionary that will contain the final author key, name pairs
    author_key_names = dict()

    # Count how many redirected records will be
    redirected_records = 0

    # For each raw pages that were returned for authors all author key and names
    # are extracted
    for filename in os.listdir(AUTHORS_DIR):

        # Find the current author page's file path
        filepath = os.path.join(AUTHORS_DIR, filename)

        # Opening the current JSON file
        data = load_json(filepath)

        # Extracting the author records
        records = data['result']

        # For each record, a check is done in case it is not an author's record
        # but a redirect instead
        for key, record in records.items():

            # If the record is a redirect then the author's right record is fetched
            if client.is_redirect(record):

                # Add to redirected records counter
                redirected_records += 1

                # Set up records filepath
                redirected_record_filename = f'redirected_{redirected_records}.json'
                redirected_record_filepath = os.path.join(AUTHORS_DIR, redirected_record_filename)

                # Fetch redirected record with built-in retries in case of errors
                results = fetch_redirected_record(
                    client=client,
                    record=record,
                    original_key=key,
                    filepath=redirected_record_filepath
                )

                # Get just the redirected record
                record = results['results']

                # Log messages to be used
                success_msg = (
                    f'AUTHORS_REDIRECTION_SUCCESS '
                    f'file={redirected_record_filename} '
                    f'attempt={results['attempts']}/{MAX_ATTEMPTS} '
                    f'duration={results['duration']:.2f}s'
                )

                error_msg = (
                    f'AUTHORS_REDIRECTION_FAILED '
                    f'error_type={results['error']} '
                    f'file={redirected_record_filename} '
                    f'attempt={results['attempts']}/{MAX_ATTEMPTS} '
                    f'duration={results['duration']:.2f}s'
                )

                # Success flag
                is_successful = results['success']

                # Log the result using the proper message and level
                log_result(
                    logger=logger,
                    is_successful=is_successful,
                    success_msg=success_msg,
                    error_msg=error_msg
                )

                # Continue to next record in case redirection failed
                if not is_successful:
                    continue

            # The current record's author name is extracted
            new_name = record['name']

            # A check is done in case alternative names for the same author key
            # are found
            if key in author_key_names:

                # Save the original name that was saved in a previous iteration
                old_name = author_key_names[key]

                # In case the previous name and the current new are different
                # a ValueError is raised
                if old_name != new_name:
                    logger.error(
                        f'Two different names \'{old_name}\' and \'{new_name}\' for author key \'{key}\' -> last name \'{new_name}\' is used.'
                    )

            # Add the author's key, name pair to the dictionary
            author_key_names[key] = new_name

    # Setting up the final JSON file's name and path
    result_filename = f'{GENRE_facet}_authors_key_name.json'
    result_filepath = os.path.join(KEYS_DIR, result_filename)

    # Save the final JSON file with the pairs
    save_json(author_key_names, result_filepath)

    logger.info(f'Finished exporting all authors\' keys and names')
