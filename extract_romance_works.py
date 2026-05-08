import os
import json
import requests
from time import sleep
from dataset_initilize import RAW_PAGES_DIR
from random import uniform

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

# Setting the connection and reading timeouts
CONNECT_TIMEOUT = 15
READ_TIMEOUT = 15
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
# --- 3. Querying Open Library API ---

# Setting the base url for querying works
# Source: https://openlibrary.org/dev/docs/api/search
base_url = 'https://openlibrary.org/search.json'

# For each page in the results save the records in JSON format
for page in range(1, MAX_PAGES+1):

    # Print a message to show progress
    print(f'({page}/{MAX_PAGES}) Extracting {GENRE} works\' metadata...', end='\r')

    # Setting the parameters for each request
    request_params = {'subject': GENRE, 'page': page, 'limit': LIMIT}

    # Try to request the records and print the error message in case of error
    try:
        response = requests.get(
            base_url,
            params=request_params,
            timeout=(CONNECT_TIMEOUT, READ_TIMEOUT)
        )
    except Exception as e:
        print(e)

    # Convert the response to JSON format
    result = response.json()

    # Set up the file name for saving the response
    filename = f'works_p{page}.json'

    # Save the response by pretty printing it with indent 4, for readability
    with open(os.path.join(GENRE_DIR, filename), mode='w') as j:
        json.dump(result, j, indent=4)

    # Politely wait more than 3 seconds for each request
    # Adding a random seconds between 0 and 1.5 to the 3, in order to simulate human behavior
    sleep(3 + uniform(0, 1.5))
# ----------------------------------------------------------------------------------
