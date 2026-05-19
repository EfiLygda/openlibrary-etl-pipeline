"""
STEP 5: Extract all editions' keys associated with a work

DETAILS:
1. Data are saved in a JSON file @ data/keys
"""
import os
from config.paths import KEYS_DIR
from config.api import GENRE_facet
from open_library import Client
from utilities.io import load_json, save_json
from utilities import wait

# Setting up thw Open Library client for querying the API
client = Client()

# Loading the file containing the general work keys
work_keys_filepath = os.path.join(KEYS_DIR, f'{GENRE_facet}_work_keys.json')
work_keys = load_json(work_keys_filepath)

# Setting up the dictionary that will contain the work keys and book keys
work_books_keys = dict()

# For each work key all book keys that are associated with it are extracted
for i, work_key in enumerate(work_keys):

    # Fetch all editions associated with the current work key
    data = client.get_work(work_key, editions=True)

    # Keep the number of editions
    # total_books = data['size']

    # Extract the book entries from the result of the query
    books = data['entries']

    # Set up the list that will contain all book keys for the current work
    current_works_book_keys = []

    # Add all book keys to the list
    for book in books:
        current_works_book_keys.append(book['key'])

    # Add the list to dictionary
    work_books_keys[work_key] = current_works_book_keys

    # Progress message
    print(f'({i+1}/{len(work_keys)}) Extracting edition keys for each general work...', end='\r')

    # Politely wait more than 5 seconds for each request
    # Adding a random seconds between 0 and 1.5 to the 3, in order to simulate human behavior
    wait(5)

# Setting up the result's filepath
result_filename = f'{GENRE_facet}_works_books_keys.json'
result_filepath = os.path.join(KEYS_DIR, result_filename)

# Save the result as a JSON file
save_json(work_books_keys, result_filepath)