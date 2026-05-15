"""
STEP 1:

DETAILS:
1.
"""

import os
import numpy as np
import pandas as pd
from config import AUTHORS_DIR, AUTHORS_STATISTICS_DIR, GENRE_facet, WORKS_DIR, CSV_DIR
import utilities as util
from open_library import JSONFileHandler, KeyHandler

# ------------------------------------------------------------------------------
# --- Authors Table ---

# Fetching all authors JSON filenames
author_files = [
    os.path.join(AUTHORS_DIR, filename)
    for filename in os.listdir(AUTHORS_DIR)
]

# Dictionary that will contain all authors' data
# Keys: author keys (i.e. '/authors/OLxxxxA')
# Values: an author's record as returned via an AUTHORS query
all_author_records = dict()

# For each file all authors' data are loaded and updated in the dictionary
for filename in author_files:

    # Load JSON authors' data
    data = JSONFileHandler.load_json(filename)

    # Update the dictionary
    all_author_records.update(data['result'])

# Convert the authors' data dictionary to a dataframe and transpose in order
# to have the author keys as index
# Notes:
# 1. the current index has values as '/authors/OLxxxxA' -> the keys are going to be denormalized
# 2. column 'key' also contains each author's keys
df_authors = pd.DataFrame(all_author_records).T

# Rename 'name' column to 'author_name'
df_authors.rename(columns={'name': 'author_name'}, inplace=True)

# Check if any of the keys are wrong
keys_are_right = (df_authors.index == df_authors.key).all()

if keys_are_right:
    print('All authors\' records were checked and author keys are right.')
else:
    print('All authors\' records were checked and some author keys are wrong.')

# Reset index as to add it as a column
# Denormalize index as to extract pure authors' key
new_index = [KeyHandler.get_key(i) for i in df_authors.index]

# Set the new denormalized index as the current index
df_authors.index = new_index

# Reset index as to now be a new column, and rename the column to 'author_key'
df_authors.reset_index(inplace=True, names='author_key')

# Column names to keep for the final table
authors_table_columns_to_keep = [
    'author_key',
    'author_name',
    'bio',
    'birth_date',
    'death_date',
]

# Keep only wanted columns
authors_table = df_authors[authors_table_columns_to_keep]

# Extract birth and death year for authors
authors_table['birth_year'] = df_authors.birth_date.apply(util.find_year)
authors_table['death_year'] = df_authors.death_date.apply(util.find_year)

# Extract authors' bio
authors_table['bio'] = authors_table.bio.apply(
    lambda x: x['value']
    if isinstance(x, dict) and 'value' in x.keys()
    else np.nan
)

# Set data types for each column
authors_dtypes = {
    'author_key': 'string',
    'author_name': 'string',
    'bio': 'string',
    'birth_date': 'string',
    'death_date': 'string',
    'birth_year': 'Int64',
    'death_year': 'Int64'
}

# Prepare tables for exporting
authors_table = util.prepare_table(
    authors_table,
    dtypes=authors_dtypes,
    primary_key='author_key',
    table_name='authors'
)

# Export table as a CSV file
# Primary key: 'author_key'
authors_table.to_csv(
    os.path.join(CSV_DIR, 'authors.csv'),
    index=False,
)

# Print a separator for current table
util.sep()
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# --- Authors Alternative Names Table ---

# Convert 'alternate_names' column that contains list of names to different rows in the dataframe
# Note: An author can have more than one alternative names
authors_alternative_names_table = df_authors[['author_key', 'alternate_names']].explode('alternate_names')

# Remove any rows tha have NaN values
# This basically refers only to 'alternate_names', in case an author does not have any 'alternate_names'
authors_alternative_names_table = authors_alternative_names_table.dropna(how='any')

# Set data types for each column
authors_alternative_names_dtypes = {
    'author_key': 'string',
    'alternate_names': 'string',
}

# Prepare tables for exporting
authors_alternative_names_table = util.prepare_table(
    df=authors_alternative_names_table,
    dtypes=authors_alternative_names_dtypes,
    primary_key=['author_key', 'alternate_names'],
    table_name='authors_alternative_names'
)

# Export table as a CSV file
# Primary key: ['author_key', 'alternate_names']
authors_alternative_names_table.to_csv(
    os.path.join(CSV_DIR, 'authors_alternative_names.csv'),
    index=False,
)

# Print a separator for current table
util.sep()
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# AUTHORS_STATISTICS_TABLE

author_statistics = JSONFileHandler.load_json(
    os.path.join(AUTHORS_STATISTICS_DIR, f'{GENRE_facet}_author_statistics.json')
)

df_stats = pd.DataFrame(author_statistics).T
df_stats.reset_index(names='author_key', inplace=True)

statistics_columns_to_keep = [
    'author_key',
    'top_work',
    'work_count',
    'ratings_count_1',
    'ratings_count_2',
    'ratings_count_3',
    'ratings_count_4',
    'ratings_count_5',
    'readinglog_count',
    'want_to_read_count',
    'currently_reading_count',
    'already_read_count',
]

author_statistics_table = df_stats[statistics_columns_to_keep]

# Print a separator for current table
util.sep()
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# WORKS_AUTHORS_TABLE

work_files = [
    os.path.join(WORKS_DIR, filename)
    for filename in os.listdir(WORKS_DIR)
]

all_works_records = dict()

for filename in work_files:
    data = JSONFileHandler.load_json(filename)
    all_works_records.update(data['result'])

df_works = pd.DataFrame(all_works_records).T

new_index = [KeyHandler.get_key(i) for i in df_works.index]
df_works.index = new_index
df_works.reset_index(inplace=True, names='work_key')

# Extract the description when needed
df_works.description = df_works.description.apply(
    lambda x: x['value'] if isinstance(x, dict) else x
)

works_authors_table = df_works[['work_key', 'authors']].explode('authors')

works_authors_table['author_key'] = works_authors_table.authors.apply(
    lambda x: KeyHandler.get_key(x['author']['key'])
    if isinstance(x, dict) and 'author' in x.keys()
    else np.nan
)
works_authors_table.drop('authors', inplace=True, axis=1)

# Print a separator for current table
util.sep()
# ------------------------------------------------------------------------------
