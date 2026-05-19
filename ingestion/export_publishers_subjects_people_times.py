"""
STEP 7: Export all publishers, subjects, people and times' names

DETAILS:
1. Data are saved in a JSON file @ data/keys
"""
import os
from config.paths import BOOKS_DIR, KEYS_DIR
from config.api import  GENRE_facet
from open_library import Client
from utilities.io import load_json, save_json

# Setting up thw Open Library client for querying the API
client = Client()

# Loading the general work keys and book keys file
books_filepaths = [
    os.path.join(BOOKS_DIR, filename)
    for filename in os.listdir(BOOKS_DIR)
]

# Dictionary that will contain all names for each field
fields = {
    'publishers': [],
    'subjects': [],
    'subject_people': [],
    'subject_times': []
}

# For each file that contain books' data the publisher name
# from each book is extracted and added to the list
for i, page in enumerate(books_filepaths):

    # Load the JSON file containing the response page with books' data
    data = load_json(page)

    # For each book, if the 'publishers' field is available the
    # publishers' names are added to the list
    for book_key, book in data['result'].items():

        # For each field, the current book's data are extracted
        for field, names in fields.items():

            # Checking if the field is available for the current book
            # and if it is the data is extracted, else a message is displayed
            if field in book.keys():
                fields[field] += book[field]
            else:
                print(f'No {field} were found for book with key \'{book_key}\'')


# Remove duplicates from each field
for field, names in fields.items():
    fields[field] = list(set(names))

# Setting up the final file's path
filename = f'{GENRE_facet}_{"__".join(fields.keys())}.json'
filepath = os.path.join(KEYS_DIR, filename)

# Exporting all publishers' names as a JSON file
save_json(fields, filepath)
