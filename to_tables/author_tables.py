"""
STEP 1: Create tables `authors`, `authors_alternative_names`, `authors_statistics` and `authors_works`
"""

import os
import numpy as np
import pandas as pd

from open_library import KeyHandler

from config.paths import AUTHORS_DIR, AUTHORS_STATISTICS_DIR, WORKS_DIR, CSV_DIR, KEYS_DIR
from config.api import GENRE_facet

from utilities.io import load_json, save_csv
from utilities.logging import sep
from utilities.parsing import find_year, extract_text
from utilities.table_prep import prepare_table
from utilities.logging import set_logger

logger = set_logger('TRANSFORM_TO_AUTHORS_TABLES')

def import_authors_to_df():
    """

    :return:
    """
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
        data = load_json(filename)

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
    keys_are_correct = (df_authors.index == df_authors.key).all()

    if keys_are_correct:
        logger.info('All authors\' records were checked and author keys are correct.')
    else:
        logger.error('All authors\' records were checked and some author keys are wrong.')

    # Reset index as to add it as a column
    # Denormalize index as to extract pure authors' key
    new_index = [KeyHandler.get_key(i) for i in df_authors.index]

    # Set the new denormalized index as the current index
    df_authors.index = new_index

    # Reset index as to now be a new column, and rename the column to 'author_key'
    df_authors.reset_index(inplace=True, names='author_key')

    return df_authors

def authors_table():
    # ------------------------------------------------------------------------------
    # --- Authors Table ---

    df_authors = import_authors_to_df()

    # Column names to keep for the final table
    authors_fields = [
        'author_key',
        'author_name',
        'bio',
        'birth_date',
        'death_date',
    ]

    # Keep only wanted columns
    authors_table = df_authors[authors_fields]

    # Extract birth and death year for authors
    authors_table['birth_year'] = df_authors.birth_date.apply(find_year)
    authors_table['death_year'] = df_authors.death_date.apply(find_year)

    # Extract authors' bio
    authors_table['bio'] = authors_table.bio.apply(extract_text)

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
    authors_table = prepare_table(
        authors_table,
        dtypes=authors_dtypes,
        primary_key='author_key',
        table_name='authors',
        # drop_na_except='author_key',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: 'author_key'
    save_csv(
        df=authors_table,
        filename='authors.csv',
        directory=CSV_DIR
    )

    # Print a separator for current table
    # sep()
    # ------------------------------------------------------------------------------

def authors_alternative_names_table():
    # ------------------------------------------------------------------------------
    # --- Authors Alternative Names Table ---

    df_authors = import_authors_to_df()

    # Convert 'alternate_names' column that contains list of names to different rows in the dataframe
    # Note: An author can have more than one alternative names
    authors_alternative_names_table = df_authors[['author_key', 'alternate_names']].explode('alternate_names')

    # Rename 'alternate_names' to 'author_alternative_name'
    authors_alternative_names_table.rename(columns={'alternate_names': 'author_alternative_name'}, inplace=True)

    # Remove any rows tha have NaN values
    # This basically refers only to 'alternate_names', in case an author does not have any 'alternate_names'
    authors_alternative_names_table = authors_alternative_names_table.dropna(how='any')

    # Set data types for each column
    authors_alternative_names_dtypes = {
        'author_key': 'string',
        'author_alternative_name': 'string',
    }

    # Prepare tables for exporting
    authors_alternative_names_table = prepare_table(
        df=authors_alternative_names_table,
        dtypes=authors_alternative_names_dtypes,
        primary_key=['author_key', 'author_alternative_name'],
        table_name='authors_alternative_names',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: ['author_key', 'author_alternative_name']
    save_csv(
        df=authors_alternative_names_table,
        filename='authors_alternative_names.csv',
        directory=CSV_DIR
    )

    # Print a separator for current table
    # sep()
    # ------------------------------------------------------------------------------

def author_statistics_table():
    # ------------------------------------------------------------------------------
    # --- Authors Statistics Table ---

    # Load JSON file with authors' statistics
    author_statistics = load_json(
        os.path.join(AUTHORS_STATISTICS_DIR, f'{GENRE_facet}_author_statistics.json')
    )

    # Convert the statistics' data dictionary to a dataframe and transpose in order
    # to have the author keys as index
    # Notes:
    # 1. the current index has values as 'OLxxxxA'
    # 2. column 'key' also contains each author's keys
    df_stats = pd.DataFrame(author_statistics).T

    # Check if any of the keys are wrong
    keys_are_correct = (df_stats.index == df_stats.key).all()

    if keys_are_correct:
        logger.info('All authors\' records were checked and author keys are correct.')
    else:
        logger.warning('All authors\' records were checked and some author keys are wrong.')

    # Reset index as to now be a new column, and rename the column to 'author_key'
    df_stats.reset_index(names='author_key', inplace=True)

    # Column names to keep
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

    # Keep only wanted columns
    author_statistics_table = df_stats[statistics_columns_to_keep]

    # Set data types for each column
    author_statistics_dtypes = {
        'author_key': 'string',
        'top_work': 'string',
        'work_count': 'Int64',
        'ratings_count_1': 'Int64',
        'ratings_count_2': 'Int64',
        'ratings_count_3': 'Int64',
        'ratings_count_4': 'Int64',
        'ratings_count_5': 'Int64',
        'readinglog_count': 'Int64',
        'want_to_read_count': 'Int64',
        'currently_reading_count': 'Int64',
        'already_read_count': 'Int64',
    }

    # Prepare tables for exporting
    author_statistics_table = prepare_table(
        author_statistics_table,
        dtypes=author_statistics_dtypes,
        primary_key='author_key',
        table_name='author_statistics',
        drop_na_except='author_key',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: 'author_key'
    save_csv(
        df=author_statistics_table,
        filename='authors_statistics.csv',
        directory=CSV_DIR
    )

    # Print a separator for current table
    # sep()
    # ------------------------------------------------------------------------------

def import_works_to_df():

    # Fetching all works JSON filenames
    work_files = [
        os.path.join(WORKS_DIR, filename)
        for filename in os.listdir(WORKS_DIR)
    ]

    # Dictionary that will contain all works' data
    # Keys: author keys (i.e. '/authors/OLxxxxW')
    # Values: an author's record as returned via an SEARCH query
    all_works_records = dict()

    # For each file all works' data are loaded and updated in the dictionary
    for filename in work_files:
        # Load JSON works' data
        data = load_json(filename)

        # Update the dictionary
        all_works_records.update(data['result'])

    # Convert the works' data dictionary to a dataframe and transpose in order
    # to have the work keys as index
    # Notes:
    # 1. the current index has values as '/authors/OLxxxxW' -> the keys are going to be denormalized
    # 2. column 'key' also contains each work's keys
    df_works = pd.DataFrame(all_works_records).T

    # Check if any of the keys are wrong
    keys_are_correct = (df_works.index == df_works.key).all()

    if keys_are_correct:
        logger.info('All works\' records were checked and works keys are correct.')
    else:
        logger.error('All works\' records were checked and some works keys are wrong.')

    # Reset index as to add it as a column
    # Denormalize index as to extract pure authors' key
    new_index = [KeyHandler.get_key(i) for i in df_works.index]

    # Set the new denormalized index as the current index
    df_works.index = new_index

    # Reset index as to now be a new column, and rename the column to 'work_key'
    df_works.reset_index(inplace=True, names='work_key')

    # Extract the description when needed
    df_works.description = df_works.description.apply(extract_text)

    return df_works

def authors_works_table():
    # ------------------------------------------------------------------------------
    # --- Works Authors Table ---

    df_works = import_works_to_df()

    # Column names to keep for the final table
    authors_works_table_columns_to_keep = [
        'authors',
        'work_key',
    ]

    # Keep only wanted columns
    authors_works_table = df_works[authors_works_table_columns_to_keep]

    # Convert 'authors' column that contains list of names to different rows in the dataframe
    # Note: A work can have more than one author
    authors_works_table = authors_works_table.explode('authors')

    # Denormalize author key (remove '/authors/')
    authors_works_table['author_key'] = authors_works_table.authors.apply(
        lambda x: KeyHandler.get_key(x['author']['key'])
        if isinstance(x, dict) and 'author' in x.keys()
        else np.nan
    )

    # Drop the authors column with the normalized author keys
    authors_works_table.drop('authors', inplace=True, axis=1)

    # Remove any rows with any NaN value (from the primary key)
    authors_works_table.dropna(how='any', inplace=True)

    # Filter works not returned from SEARCH
    valid_work_keys = load_json(
        os.path.join(KEYS_DIR, 'romance_fiction_work_keys.json')
    )
    authors_works_table = authors_works_table[authors_works_table.work_key.isin(valid_work_keys)]

    # Reorder columns
    authors_works_table = authors_works_table[
        [
            'author_key',
            'work_key'
        ]
    ]

    # Set data types for each column
    authors_works_dtypes = {
        'work_key': 'string',
        'author_key': 'string',
    }

    # Prepare tables for exporting
    authors_works_table = prepare_table(
        authors_works_table,
        dtypes=authors_works_dtypes,
        primary_key=['work_key', 'author_key'],
        table_name='authors_works',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: ['work_key', 'author_key']
    save_csv(
        df=authors_works_table,
        filename='authors_works.csv',
        directory=CSV_DIR
    )

    # Print a separator for current table
    # sep()
    # ------------------------------------------------------------------------------


def run():
    authors_table()
    authors_alternative_names_table()
    author_statistics_table()
    authors_works_table()