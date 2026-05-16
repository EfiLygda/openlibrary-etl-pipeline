"""
STEP 2: Create tables `editions`, `editions_contributors`, `editions_publishing`,
        `content_publishing` and `content_details`
"""

import os
import numpy as np
import pandas as pd
from config import AUTHORS_DIR, AUTHORS_STATISTICS_DIR, GENRE_facet, WORKS_DIR, CSV_DIR, BOOKS_DIR
import utilities as util
from open_library import JSONFileHandler, KeyHandler

# region
# ------------------------------------------------------------------------------
# --- Editions Table ---

# Fetching all editions/books JSON filenames
books_files = [
    os.path.join(BOOKS_DIR, filename)
    for filename in os.listdir(BOOKS_DIR)
]

# Dictionary that will contain all books' data
# Keys: books keys (i.e. '/books/OLxxxxM')
# Values: a book's record as returned via an BOOKS query
all_books_records = dict()

# For each file all books' data are loaded and updated in the dictionary
for filename in books_files:

    # Load JSON books' data
    data = JSONFileHandler.load_json(filename)

    # Update the dictionary
    all_books_records.update(data['result'])

# Convert the books' data dictionary to a dataframe and transpose in order
# to have the author keys as index
# Notes:
# 1. the current index has values as '/books/OLxxxxA' -> the keys are going to be denormalized
# 2. column 'key' also contains each book's keys
df_books = pd.DataFrame(all_books_records).T

# Check if any of the keys are wrong
keys_are_correct = (df_books.index == df_books.key).all()

if keys_are_correct:
    print('All editions\' records were checked and edition keys are correct.')
else:
    print('All editions\' records were checked and some editions\' keys are wrong.')

# Reset index as to add it as a column
# Denormalize index as to extract pure books' key
new_index = [KeyHandler.get_key(i) for i in df_books.index]

# Set the new denormalized index as the current index
df_books.index = new_index

# Reset index as to now be a new column, and rename the column to 'edition_key'
df_books.reset_index(inplace=True, names='edition_key')

# Separate for each of the final editions tables fields and data
# Column names to keep for each of the final tables
editions_fields = [
    'edition_key', # 'key', # edition key
    "works", # contains work key -> normalize and rename to work_key
    "title",
    "subtitle",
    "edition_name",
]

contributors_fields = [
    'edition_key', # 'key'
    "contributors",
    "by_statement",
    "translated_from",
    "translation_of",
]

publishing_fields = [
    'edition_key', # 'key'
    "publish_date",
    "publishers",
    "publish_places",
    "publish_country",
    "series", # name not key
]

content_fields = [
    'edition_key', # 'key'
    "description",
    "notes",
    "first_sentence",
]

details_fields = [
    'edition_key', # 'key'
    "number_of_pages",
    "physical_format",
    "physical_dimensions",
    "weight",
    "languages",
]

# endregion

# Keep only wanted columns for each table
editions_table = df_books[editions_fields]
contributors_table = df_books[contributors_fields]
publishing_table = df_books[publishing_fields]
content_table = df_books[content_fields]
details_table = df_books[details_fields]
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# --- Editions Table ---
# region
# Extract work keys for each edition
# Check if more than one works referred to an edition -> Answer: FALSE
util.check_explode(
    col=editions_table.works,
    table_name='editions'
)

# Work keys are stored denormalized (i.e. OLxxxxW)
editions_table['works'] = editions_table.works.apply(
    lambda x: KeyHandler.get_key(x[0]['key'])
)

# Remove 'works' column
editions_table.rename(columns={'works': 'work_key'}, inplace=True)

# Set data types for each column
editions_dtypes = {
    'edition_key': 'string',
    "work_key": 'string',
    "title": 'string',
    "subtitle": 'string',
    "edition_name": 'string',
}

# Prepare tables for exporting
editions_table = util.prepare_table(
    editions_table,
    dtypes=editions_dtypes,
    primary_key='edition_key',
    table_name='editions',
    drop_na_except = 'edition_key',
    drop_duplicates = True,
)

# Export table as a CSV file
# Primary key: 'edition_key'
editions_table.to_csv(
    os.path.join(CSV_DIR, 'editions.csv'),
    index=False,
)

# Print a separator for current table
util.sep()
# ------------------------------------------------------------------------------
# endregion


# ------------------------------------------------------------------------------
# --- Contributors Table ---
# region
# Check if any row in 'contributors' has more than one contributor -> Answer: True
util.check_explode(
    col=contributors_table.contributors,
    table_name='contributors'
)

# 'contributors' is exploded as to have one contributor per row for some editions
contributors_table = contributors_table.explode(column='contributors')

# Extract contributor name and role to two separate columns
contributors_table[['contributor_name', 'contributor_role']] = contributors_table.contributors.apply(
    lambda x: pd.Series([x['name'], x['role']])
    if isinstance(x, dict) and 'name' in x.keys() and 'role' in x.keys()
    else pd.Series([np.nan, np.nan])
)

# Drop 'contributors' column from table
contributors_table.drop('contributors', inplace=True, axis=1)

# Check if any row in 'translated_from' has more than one contributor -> Answer: False
util.check_explode(
    col=contributors_table.translated_from,
    table_name='translated_from'
)

# Extract the language from 'translated_from'
contributors_table['translated_from'] = contributors_table.translated_from.apply(
    lambda x: util.get_language(x[0]['key'])
    if isinstance(x, list)
    else np.nan
)

# Reorder columns
contributors_table = contributors_table[
    [
        'edition_key',
        'contributor_name',
        'contributor_role',
        'by_statement',
        'translated_from',
        'translation_of',

    ]
]

# Set data types for each column
contributors_dtypes = {
    'edition_key': 'string',
    "contributor_name": 'string',
    "contributor_role": 'string',
    "by_statement": 'string',
    "translation_of": 'string',
    "translated_from": 'string',
}

# Prepare tables for exporting
contributors_table = util.prepare_table(
    contributors_table,
    dtypes=contributors_dtypes,
    primary_key=None,
    table_name='contributors',
    drop_na_except='edition_key',
    drop_duplicates=True,
)

# Export table as a CSV file
# Primary key: None
contributors_table.to_csv(
    os.path.join(CSV_DIR, 'contributors.csv'),
    index=False,
)

# Print a separator for current table
util.sep()
# ------------------------------------------------------------------------------
# endregion

# ------------------------------------------------------------------------------
# --- Publishing Table ---
# region

# Extract the publishing year form publish_date
publishing_table['publish_year'] = publishing_table.publish_date.apply(util.find_year)

# Check if more than one publisher name is referred to an edition -> Answer: TRUE
util.check_explode(
    col=publishing_table.publishers,
    table_name='publishing'
)

# 'publishers' is exploded as to have one publisher per row for some editions
publishing_table = publishing_table.explode('publishers')

# Rename 'publishers'
publishing_table.rename(columns={'publishers': 'publisher'}, inplace=True)

# Check if more than one publish_places name is referred to an edition -> Answer: TRUE
util.check_explode(
    col=publishing_table.publish_places,
    table_name='publish_places'
)

# 'publish_places' is exploded as to have one publish place per row for some editions
publishing_table = publishing_table.explode('publish_places')

# Rename 'publish_places'
publishing_table.rename(columns={'publish_places': 'publish_place'}, inplace=True)

# Check if more than one publish_places name is referred to an edition -> Answer: TRUE
util.check_explode(
    col=publishing_table.series,
    table_name='series'
)

# 'publish_places' is exploded as to have one publish place per row for some editions
publishing_table = publishing_table.explode('series')

# Set data types for each column
publishing_dtypes = {
    'edition_key': 'string',
    "publish_date": 'string',
    "publisher": 'string',
    "publish_place": 'string',
    "publish_country": 'string',
    "series": 'string',
    "publish_year": "Int64"
}

# Prepare tables for exporting
publishing_table = util.prepare_table(
    publishing_table,
    dtypes=publishing_dtypes,
    primary_key=None,
    table_name='publishing',
    drop_na_except = 'edition_key',
    drop_duplicates = True,
)

# Export table as a CSV file
# Primary key: 'edition_key'
publishing_table.to_csv(
    os.path.join(CSV_DIR, 'publishing.csv'),
    index=False,
)

# Print a separator for current table
util.sep()
# ------------------------------------------------------------------------------
# endregion