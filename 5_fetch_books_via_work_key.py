"""
STEP 5:

DETAILS:
1.
"""
import os
from time import sleep
from random import uniform
from config import KEYS_DIR, GENRE_facet
from open_library import Client, JSONFileHandler

# Setting up thw Open Library client for querying the API
client = Client()

work_keys_filepath = os.path.join(KEYS_DIR, 'romance_fiction_work_keys.json')
work_keys = JSONFileHandler.load_json(work_keys_filepath)

work_books_keys = dict()

for i, work_key in enumerate(work_keys):
    data = client.get_work(work_key, editions=True)

    total_books = data['size']

    books = data['entries']

    current_works_book_keys = []

    for book in books:
        current_works_book_keys.append(book['key'])

    work_books_keys[work_key] = current_works_book_keys

    print(f'({i+1}/{len(work_keys)}) Extracting edition keys for each general work...', end='\r')

    # Politely wait more than 5 seconds for each request
    # Adding a random seconds between 0 and 1.5 to the 3, in order to simulate human behavior
    sleep(5 + uniform(0, 1.5))

result_filename = f'{GENRE_facet}_works_books_keys.json'
result_filepath = os.path.join(KEYS_DIR, result_filename)
JSONFileHandler.save_json(work_books_keys, result_filepath)