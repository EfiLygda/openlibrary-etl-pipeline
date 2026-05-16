"""
STEP 3: Create tables `works`, `works_series` and `series` tables
"""

import os
import numpy as np
import pandas as pd
from config import CSV_DIR, BOOKS_DIR, WORKS_DIR, SEARCH_DIR
import utilities as util
from open_library import JSONFileHandler, KeyHandler

# ------------------------------------------------------------------------------
# --- Import and convert to dictionaries all works and enriched works' data ---
# region
# Fetching all works and works enriched JSON filenames
works_files = [
    os.path.join(SEARCH_DIR, filename)
    for filename in os.listdir(SEARCH_DIR)
]

works_enriched_files = [
    os.path.join(WORKS_DIR, filename)
    for filename in os.listdir(WORKS_DIR)
]

# Dictionaries that will contain all works' data
# Keys: works keys (i.e. '/books/OLxxxxW')
# Values: a work's record as returned via an SEARCH query
all_works_records = dict()

# For each file all works' data are loaded and updated in the dictionary
for filename in works_files:

    # Load JSON books' data
    data = JSONFileHandler.load_json(filename)

    records = data['docs']

    for record in data['docs']:
        if record['key'] in all_works_records.keys():
            print(f'{record['key']} is duplicate.')
        else:
            all_works_records[record['key']] = record


# Keys: works keys (i.e. '/books/OLxxxxW')
# Values: a work's record as returned via an WORKS query
all_works_enriched_records = dict()

# For each file all enriched works' data are loaded and updated in the dictionary
for filename in works_enriched_files:

    # Load JSON books' data
    data = JSONFileHandler.load_json(filename)

    # Update the dictionary
    all_works_enriched_records.update(data['result'])

# Print a separator
util.sep()
# ------------------------------------------------------------------------------
# endregion

# ------------------------------------------------------------------------------
# --- Convert dictionaries to dataframes and merge ---
# region
# Convert the works' data dictionary to a dataframe and transpose in order
# to have the author keys as index
# Notes:
# 1. the current index has values as '/works/OLxxxxW' -> the keys are going to be denormalized
# 2. column 'key' also contains each work's keys
df_works = pd.DataFrame(all_works_records).T
df_works_enriched = pd.DataFrame(all_works_enriched_records).T

# Join the two dataframes on the 'key' column
df_works_all = df_works.merge(df_works_enriched, how='left', on='key', suffixes=('', '__enriched'))

df_works_all.columns