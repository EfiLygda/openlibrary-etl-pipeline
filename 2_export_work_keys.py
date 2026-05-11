import os
import json
from config import RAW_PAGES_DIR, GENRE_facet, KEYS_DIR, WORKS_DIR
from OpenLibrary import OpenLibraryClient

client = OpenLibraryClient()

# DIR = os.path.join(RAW_PAGES_DIR, GENRE_facet)

WORKS_KEYS = []
AUTHOR_KEYS = []
SERIES_KEYS = []

for file in os.listdir(WORKS_DIR):

    filename = os.path.join(WORKS_DIR,file)

    with open(filename, mode='r', encoding='utf-8') as j:
        data = json.load(j)

    for record in data['docs']:
        # print(record)

        if 'key' in record.keys():
            WORKS_KEYS += [record['key'].replace('/works/', '')]

        if 'author_key' in record.keys():
            AUTHOR_KEYS += record['author_key']

        if 'series_key' in record.keys():
            SERIES_KEYS += record['series_key']

key_lists = [WORKS_KEYS, AUTHOR_KEYS, SERIES_KEYS]
key_types = ['work_keys', 'author_keys', 'series_keys']

for key_list, key_type in zip(key_lists, key_types):

    unique_keys = list(set(key_list))

    filename = os.path.join(KEYS_DIR, f'{GENRE_facet}_{key_type}.json')

    client.save_json(unique_keys, filename)


