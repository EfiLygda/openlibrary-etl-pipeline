"""
STEP 3: Create tables `works`, `works_series` and `series` tables
"""

import os
from unittest.mock import inplace

import numpy as np
import pandas as pd
from config import CSV_DIR, BOOKS_DIR, WORKS_DIR, SEARCH_DIR, SERIES_DIR
import utilities as util
from open_library import JSONFileHandler, KeyHandler

# ------------------------------------------------------------------------------
# --- Import and convert to dictionaries all works, enriched works' and series data ---
# region
# Fetching all works, works enriched and series JSON filenames
works_files = [
    os.path.join(SEARCH_DIR, filename)
    for filename in os.listdir(SEARCH_DIR)
]

works_enriched_files = [
    os.path.join(WORKS_DIR, filename)
    for filename in os.listdir(WORKS_DIR)
]

series_files = [
    os.path.join(SERIES_DIR, filename)
    for filename in os.listdir(SERIES_DIR)
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

# Keys: series keys (i.e. '/books/OLxxxxL')
# Values: a series' record as returned via an WORKS query
all_series_records = dict()

# For each file all enriched series' data are loaded and updated in the dictionary
for filename in series_files:

    # Load JSON books' data
    data = JSONFileHandler.load_json(filename)

    # Update the dictionary
    all_series_records.update(data['result'])

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

# Convert the series' data dictionary to a dataframe and transpose in order
df_series = pd.DataFrame(all_series_records).T

# endregion

# ------------------------------------------------------------------------------
# --- Change column names and drop columns ---
# region

# Rename works 'key' to 'work_key'
df_works_all.rename(columns={'key': 'work_key'}, inplace=True)

# Denormalize 'work_key'
df_works_all['work_key'] = df_works_all.work_key.apply(KeyHandler.get_key)

# Check if 'title' == 'title__enriched' and 'subtitle' == 'subtitle__enriched' -> Answer: TRUE
if (df_works_all.title == df_works_all.title__enriched).all():
    print('\'title\' and \'title__enriched\' have the same values')
    df_works_all.drop('title__enriched', inplace=True, axis=1)

if (df_works_all.dropna().subtitle == df_works_all.dropna().subtitle__enriched).all():
    print('\'subtitle\' and \'subtitle__enriched\' have the same values')
    df_works_all.drop('subtitle__enriched', inplace=True, axis=1)

# Reset index and drop the new column
df_series.reset_index(inplace=True, drop=True)

# Rename works 'key' to 'series_key'
df_series.rename(columns={'key': 'series_key'}, inplace=True)

# Denormalize 'series_key'
df_series['series_key'] = df_series.series_key.apply(KeyHandler.get_key)

# endregion

# ------------------------------------------------------------------------------
# --- Separate to different tables ---
# region

# Set the different fields for each table
works_fields = [
    'work_key',
    'title',
    'subtitle',
    'description',
    'first_sentence',
    'edition_count',
    'first_publish_year',
    'first_publish_date',
]

series_fields = [
    'work_key',
    'series_key',
    'series_position', # add series name
]

availability_fields = [
    'work_key',
    'ebook_access',
    'has_fulltext',
    'public_scan_b',
]

subjects_fields = [
    'work_key',
    'subjects',
]

people_fields = [
    'work_key',
    'subject_people',
]

places_fields = [
    'work_key',
    'subject_places',
]

times_fields = [
    'work_key',
    'subject_times',
]

# endregion

# Keep only wanted columns for each table
works_table = df_works_all[works_fields]
series_table = df_works_all[series_fields]
availability_table = df_works_all[availability_fields]
subjects_table = df_works_all[subjects_fields]
people_table = df_works_all[people_fields]
places_table = df_works_all[places_fields]
times_table = df_works_all[times_fields]

# ------------------------------------------------------------------------------
# --- Works Table ---
# region
# Extract 'description' text
works_table['description'] = works_table.description.apply(util.extract_text)

# Extract 'first_sentence' text
works_table['first_sentence'] = works_table.first_sentence.apply(util.extract_text)

# Set data types for each column
works_dtypes = {
    'work_key': 'string',
    "title": 'string',
    "subtitle": 'string',
    "description": 'string',
    "first_sentence": 'string',
    "edition_count": 'Int64',
    "first_publish_year": 'Int64',
    "first_publish_date": 'string',
}

# Prepare tables for exporting
works_table = util.prepare_table(
    works_table,
    dtypes=works_dtypes,
    primary_key='work_key',
    table_name='works',
    drop_na_except = 'work_key',
    drop_duplicates = True,
)

# Export table as a CSV file
# Primary key: 'work_key'
works_table.to_csv(
    os.path.join(CSV_DIR, 'works.csv'),
    index=False,
)

# Print a separator for current table
util.sep()
# ------------------------------------------------------------------------------
# endregion

# ------------------------------------------------------------------------------
# --- Series Table ---
# region

# Check if more than one series_key referred to a work -> Answer: FALSE
util.check_explode(
    col=series_table.series_key,
    table_name='series'
)

# Extract 'series_key'
series_table['series_key'] = series_table.series_key.apply(
    lambda x: x[0]
    if isinstance(x, list)
    else np.nan
)

# Check if more than one series_position referred to a work -> Answer: FALSE
util.check_explode(
    col=series_table.series_position,
    table_name='series'
)

# Extract 'series_key'
series_table['series_position'] = series_table.series_position.apply(
    lambda x: x[0]
    if isinstance(x, list)
    else np.nan
)

# Add series names to the series table
series_table = series_table.merge(
    df_series[['series_key', 'name']],
    on='series_key',
    how='left'
)

# Set data types for each column
series_dtypes = {
    'work_key': 'string',
    "series_key": 'string',
    "series_position": 'string',
    "name": 'string',
}

# Prepare tables for exporting
series_table = util.prepare_table(
    series_table,
    dtypes=series_dtypes,
    primary_key='work_key',
    table_name='series',
    drop_na_except = ['work_key','series_key'],
    drop_duplicates = True,
)

# Export table as a CSV file
# Primary key: 'work_key'
series_table.to_csv(
    os.path.join(CSV_DIR, 'works_series.csv'),
    index=False,
)

# Print a separator for current table
util.sep()
# ------------------------------------------------------------------------------
# endregion

# ------------------------------------------------------------------------------
# --- Availability Table ---
# region

# Rename 'public_scan_b' to 'has_public_scan'
availability_table.rename(columns={'public_scan_b': 'has_public_scan'}, inplace=True)


# Set data types for each column
availability_dtypes = {
    'work_key': 'string',
    "ebook_access": 'string',
    "has_fulltext": 'bool',
    "has_public_scan": 'bool',
}

# Prepare tables for exporting
availability_table = util.prepare_table(
    availability_table,
    dtypes=availability_dtypes,
    primary_key='work_key',
    table_name='availability',
    drop_na_except = 'work_key',
    drop_duplicates = True,
)

# Export table as a CSV file
# Primary key: 'work_key'
availability_table.to_csv(
    os.path.join(CSV_DIR, 'works_availability.csv'),
    index=False,
)

# Print a separator for current table
util.sep()
# ------------------------------------------------------------------------------
# endregion

# ------------------------------------------------------------------------------
# --- Subjects Table ---
# region

# Check if more than one 'subjects' referred to a work -> Answer: TRUE
util.check_explode(
    col=subjects_table.subjects,
    table_name='subjects'
)

# Explode 'subjects'
subjects_table = subjects_table.explode(column='subjects')

# Rename 'subjects' to 'subject'
subjects_table.rename(columns={'subjects': 'subject'}, inplace=True)

# Set data types for each column
subjects_dtypes = {
    'work_key': 'string',
    "subject": 'string',
}

# Prepare tables for exporting
subjects_table = util.prepare_table(
    subjects_table,
    dtypes=subjects_dtypes,
    primary_key=['work_key','subject'],
    table_name='subjects',
    drop_na_except = 'work_key',
    drop_duplicates = True,
)

# Export table as a CSV file
# Primary key: 'work_key','subject'
subjects_table.to_csv(
    os.path.join(CSV_DIR, 'works_subjects.csv'),
    index=False,
)

# Print a separator for current table
util.sep()
# ------------------------------------------------------------------------------
# endregion
