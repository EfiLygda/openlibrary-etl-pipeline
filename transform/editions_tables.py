"""
STEP 2: Create tables `editions`, `editions_contributors`, `editions_publishing`,
        `editions_publishing` and `editions_details`
"""

import os
import numpy as np
import pandas as pd
from config.paths import CSV_DIR, BOOKS_DIR
from utilities.io import load_json
from utilities.logging import sep
from utilities.validation import check_explode
from utilities.parsing import get_language, find_year, extract_text
from utilities.table_prep import prepare_table
from open_library import KeyHandler

# ------------------------------------------------------------------------------
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
    data = load_json(filename)

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

# Keep only wanted columns for each table
editions_table = df_books[editions_fields]
contributors_table = df_books[contributors_fields]
publishing_table = df_books[publishing_fields]
contents_table = df_books[content_fields]
details_table = df_books[details_fields]
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# --- Editions Table ---

# Extract work keys for each edition
# Check if more than one works referred to an edition -> Answer: FALSE
check_explode(
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
editions_table = prepare_table(
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
sep()
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# --- Contributors Table ---

# Check if any row in 'contributors' has more than one contributor -> Answer: True
check_explode(
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
check_explode(
    col=contributors_table.translated_from,
    table_name='translated_from'
)

# Extract the language from 'translated_from'
contributors_table['translated_from'] = contributors_table.translated_from.apply(
    lambda x: get_language(x[0]['key'])
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
contributors_table = prepare_table(
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
    os.path.join(CSV_DIR, 'editions_contributors.csv'),
    index=False,
)

# Print a separator for current table
sep()
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# --- Publishing Table ---

# Extract the publishing year form publish_date
publishing_table['publish_year'] = publishing_table.publish_date.apply(find_year)

# Check if more than one publisher name is referred to an edition -> Answer: TRUE
check_explode(
    col=publishing_table.publishers,
    table_name='publishing'
)

# 'publishers' is exploded as to have one publisher per row for some editions
publishing_table = publishing_table.explode('publishers')

# Rename 'publishers'
publishing_table.rename(columns={'publishers': 'publisher'}, inplace=True)

# Check if more than one publish_places name is referred to an edition -> Answer: TRUE
check_explode(
    col=publishing_table.publish_places,
    table_name='publish_places'
)

# 'publish_places' is exploded as to have one publish place per row for some editions
publishing_table = publishing_table.explode('publish_places')

# Rename 'publish_places'
publishing_table.rename(columns={'publish_places': 'publish_place'}, inplace=True)

# Check if more than one publish_places name is referred to an edition -> Answer: TRUE
check_explode(
    col=publishing_table.series,
    table_name='series'
)

# 'publish_places' is exploded as to have one publish place per row for some editions
publishing_table = publishing_table.explode('series')

# Reorder columns
publishing_table = publishing_table[
    [
        'edition_key',
        'publish_date',
        'publish_year',
        'publisher',
        'publish_place',
        'publish_country',
        'series',
    ]
]

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
publishing_table = prepare_table(
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
    os.path.join(CSV_DIR, 'editions_publishing.csv'),
    index=False,
)

# Print a separator for current table
sep()
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# --- Contents Table ---

# Extract description
contents_table['description'] = contents_table.description.apply(extract_text)

# Extract notes
contents_table['notes'] = contents_table.notes.apply(extract_text)

# Extract first sentence
contents_table['first_sentence'] = contents_table.first_sentence.apply(extract_text)

# Set data types for each column
contents_dtypes = {
    'edition_key': 'string',
    "description": 'string',
    "notes": 'string',
    "first_sentence": 'string',
}

# Prepare tables for exporting
contents_table = prepare_table(
    contents_table,
    dtypes=contents_dtypes,
    primary_key='edition_key',
    table_name='contents',
    drop_na_except = 'edition_key',
    drop_duplicates = True,
)

# Export table as a CSV file
# Primary key: 'edition_key'
contents_table.to_csv(
    os.path.join(CSV_DIR, 'editions_contents.csv'),
    index=False,
)

# Print a separator for current table
sep()
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# --- Editions Table ---

# Check if more than one language referred to an edition -> Answer: FALSE
check_explode(
    col=details_table.languages,
    table_name='details'
)

# 'languages' is exploded as to have one language per row for some editions
details_table = details_table.explode('languages')

# Extract languages
details_table['languages'] = details_table.languages.apply(
    lambda x: get_language(x['key'])
    if isinstance(x, dict) and 'key' in x.keys()
    else np.nan
)

# Rename 'languages' column
details_table.rename(columns={'languages': 'language'}, inplace=True)

# Set data types for each column
details_dtypes = {
    'edition_key': 'string',
    "number_of_pages": 'Int64',
    "physical_format": 'string',
    "physical_dimensions": 'string',
    "weight": 'string',
    "language": 'string',
}

# Prepare tables for exporting
details_table = prepare_table(
    details_table,
    dtypes=details_dtypes,
    # primary_key='edition_key',
    table_name='details',
    drop_na_except = 'edition_key',
    drop_duplicates = True,
)

# Export table as a CSV file
# Primary key: 'edition_key'
details_table.to_csv(
    os.path.join(CSV_DIR, 'editions_details.csv'),
    index=False,
)

# Print a separator for current table
sep()
# ------------------------------------------------------------------------------
