"""
STEP 7: Export all publishers' names

DETAILS:
1. Data are saved in a JSON file @ data/keys
"""
import os
from config import  BOOKS_DIR, KEYS_DIR
from open_library import Client, JSONFileHandler

# Setting up thw Open Library client for querying the API
client = Client()

# Loading the general work keys and book keys file
books_filepaths = [
    os.path.join(BOOKS_DIR, filename)
    for filename in os.listdir(BOOKS_DIR)
]

# List that will contain all publisher names
publisher_names = []

# For each file that contain books' data the publisher name
# from each book is extracted and added to the list
for i, page in enumerate(books_filepaths):

    # Load the JSON file containing the response page with books' data
    data = JSONFileHandler.load_json(page)

    # For each book, if the 'publishers' field is available the
    # publishers' names are added to the list
    for book_key, book in data['result'].items():

        # Checking if the 'publishers' field is available for the current book
        if 'publishers' in book.keys():
            publisher_names += book['publishers']
        else:
            print(f'No publishers were found for book with key \'{book_key}\'')

# Remove duplicates from publishers' names
unique_publishers = tuple(publisher_names)

# Setting up the final file's path
filename = f'publishers.json'
filepath = os.path.join(KEYS_DIR, filename)

# Exporting all publishers' names as a JSON file
JSONFileHandler.save_json(unique_publishers, filepath)
