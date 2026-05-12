"""
STEP 2: Export all work, author and series keys from the works that were fetched from STEP 1

DETAILS:
1. No querying the API is done. Using only the JSON files extracted from STEP 1
2. Work, author and series keys as well as author key and name pairs are saved
   as JSON files @ data/keys
"""

import os
import json
from config import GENRE_facet, KEYS_DIR, SEARCH_DIR
from open_library import JSONFileHandler

# Define list that will contain all work, author and series keys
WORKS_KEYS = []
AUTHOR_KEYS = []
SERIES_KEYS = []

# For each file all general works, authors and series keys will be extracted
# from the pages of records returned via SEARCH
for current_page in os.listdir(SEARCH_DIR):

    # Define current files path (each file is a page of records)
    filename = os.path.join(SEARCH_DIR, current_page)

    # Load each works record returned via SEARCH
    data = JSONFileHandler.load_json(filename)

    # For each record/general work in current page add in the list
    # its work, author and series key is added to the lists
    for record in data['docs']:

        if 'key' in record.keys():
            WORKS_KEYS += [record['key'].replace('/works/', '')]

        if 'author_key' in record.keys():
            AUTHOR_KEYS += record['author_key']

        if 'series_key' in record.keys():
            SERIES_KEYS += record['series_key']

# Setting up lists to be zipped for iterating at the same time
# in order to save their contents
key_lists = [WORKS_KEYS, AUTHOR_KEYS, SERIES_KEYS]
key_types = ['work_keys', 'author_keys', 'series_keys']
unique_key_counts = dict()

# For each key list and key type pair the unique keys are saved as JSON files
for key_list, key_type in zip(key_lists, key_types):

    # Remove duplicates from each key list
    unique_keys = list(set(key_list))

    # Keep the unique count of keys
    unique_key_counts[key_type] = len(unique_keys)

    # Define each JSON file's path
    filename = os.path.join(KEYS_DIR, f'{GENRE_facet}_{key_type}.json')

    # Save each JSON file
    JSONFileHandler.save_json(unique_keys, filename)

# Print results counts
print(
    f'Extracted {unique_key_counts['work_keys']} general works,'
    f' {unique_key_counts['author_keys']} authors'
    f' and {unique_key_counts['series_keys']} series!'
)