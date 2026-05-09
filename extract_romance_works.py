import os
from time import sleep
from dataset_initilize import RAW_PAGES_DIR
from random import uniform
from OpenLibrary import OpenLibraryClient

# ----------------------------------------------------------------------------------
# --- 1. Setting up the genre directories ---
GENRE = 'romance fiction'

# A normalized version of the genre used for filenames and directories
GENRE_facet = GENRE.replace(' ', '_')

# Creating the raw files directory, if it does not already exists
GENRE_DIR = os.path.join(RAW_PAGES_DIR, GENRE_facet)
if not os.path.exists(GENRE_DIR):
    os.makedirs(GENRE_DIR)
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- 2. Parameters for quering the API ---
# Limiting to 100 records per page and maximum 20 pages
# Final record number: 2000
LIMIT = 100
MAX_PAGES = 20
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- 3. Querying Open Library API ---

# Setting up an Open Library Client for querying the API
client = OpenLibraryClient()

# Setting the page limit
client.LIMIT = LIMIT

# For each page in the results save the records in JSON format
for page in range(1, MAX_PAGES+1):

    # Print a message to show progress
    print(f'({page}/{MAX_PAGES}) Extracting {GENRE} works\' metadata...', end='\r')

    # Set up the file name for saving the response
    filename = f'works_p{page}.json'
    filepath = os.path.join(GENRE_DIR, filename)

    # Save the response as a JSON file
    client.save_search(filename=filepath, subject=GENRE, page=page)

    # Politely wait more than 3 seconds for each request
    # Adding a random seconds between 0 and 1.5 to the 3, in order to simulate human behavior
    sleep(3 + uniform(0, 1.5))
# ----------------------------------------------------------------------------------
