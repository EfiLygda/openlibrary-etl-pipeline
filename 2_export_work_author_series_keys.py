import os
import json
from config import GENRE_facet, KEYS_DIR, SEARCH_DIR
from OpenLibrary import OpenLibraryClient

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
    with open(filename, mode='r', encoding='utf-8') as j:
        data = json.load(j)

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

# For each key list and key type pair the unique keys are saved as JSON files
for key_list, key_type in zip(key_lists, key_types):

    # Remove duplicates from each key list
    unique_keys = list(set(key_list))

    # Define each JSON file's path
    filename = os.path.join(KEYS_DIR, f'{GENRE_facet}_{key_type}.json')

    # Save each JSON file
    OpenLibraryClient.save_json(unique_keys, filename)

print(f'Extracted {len(WORKS_KEYS)} general works, {len(AUTHOR_KEYS)} authors and {len(SERIES_KEYS)} series!')