"""
STEP 1: Fetch and extract general works under the GERNE via Open Library API's SEARCH

DETAILS:
1. Not all works are extracted, config.LIMIT, config.MAX_PAGES are used as to not overload the API
2. GERNE refers to config.api.GENRE
3. The query uses the SEARCH basic url (See example SEARCH @ API_info/base_urls)
4. All pages of records are saved as JSON files @ data/raw_pages/{GERNE}/works
"""

import os
from utilities.rate_limit import wait
from open_library import Client
from config.paths import SEARCH_DIR
from config.api import LIMIT, MAX_PAGES, GENRE, GENRE_facet

# ----------------------------------------------------------------------------------
# --- Querying Open Library API ---

# Setting up an Open Library Client for querying the API
client = Client()

# Setting the page limit
client.LIMIT = LIMIT

# For each page in the results save the records in JSON format
for page in range(1, MAX_PAGES+1):

    # Print a message to show progress
    print(f'({page}/{MAX_PAGES}) Extracting {GENRE} works\' metadata...', end='\r')

    # Set up the file name for saving the response
    filename = f'SEARCH_p{page}.json'
    filepath = os.path.join(SEARCH_DIR, filename)

    # Save the response as a JSON file
    client.save_search(filename=filepath, subject=GENRE_facet, page=page)

    # Politely wait more than 3 seconds for each request
    # Adding a random seconds between 0 and 1.5 to the 3, in order to simulate human behavior
    wait(3)
# ----------------------------------------------------------------------------------
