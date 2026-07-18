"""
STEP 2: Create tables `editions`, `editions_contributors`, `editions_publishing`,
        `editions_publishing` and `editions_details`
"""

import os
import numpy as np
import pandas as pd

from data_pipeline.open_library import KeyHandler

from config.paths import CSV_DIR, BOOKS_DIR, KEYS_DIR

from utilities.io import load_json, save_csv
from data_pipeline.utils.data.validation import check_explode
from data_pipeline.utils.data.parsing import get_language, find_year, extract_text
from etl.transform.dtypes import (editions_dtypes,
                                  contributors_dtypes,
                                  publishing_dtypes,
                                  contents_dtypes,
                                  details_dtypes)
from data_pipeline.utils.data.table_prep import prepare_table
from utilities.logging import set_logger

logger = set_logger('TRANSFORM_TO_EDITIONS_TABLES')

def import_editions_data() -> list[pd.DataFrame]:
    """
    Function for importing all editions' data and splitting them to 5 dataframes:

    1. editions table,
    2. contributors table,
    3. publishing table,
    4. contents table,
    5. details table

    :return: list[pd.DataFrame], list with the 5 dataframes
    """
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
        all_books_records.update(data)

    # Convert the books' data dictionary to a dataframe and transpose in order
    # to have the author keys as index
    # Notes:
    # 1. the current index has values as '/books/OLxxxxA' -> the keys are going to be denormalized
    # 2. column 'key' also contains each book's keys
    df_books = pd.DataFrame(all_books_records).T

    # Check if any of the keys are wrong
    keys_are_correct = (df_books.index == df_books.key).all()

    if keys_are_correct:
        logger.info('EDITION_KEYS_VALIDATION_SUCCESS')
    else:
        logger.error('EDITION_KEYS_VALIDATION_FAILED')

    # Reset index as to add it as a column
    # Denormalize index as to extract pure books' key
    new_index = [KeyHandler.get_key(i) for i in df_books.index]

    # Set the new denormalized index as the current index
    df_books.index = new_index

    # Reset index as to now be a new column, and rename the column to 'edition_key'
    df_books.reset_index(inplace=True, names='edition_key')

    # Extract work keys for each edition
    # Check if more than one works referred to an edition -> Answer: FALSE
    check_explode(
        col=df_books.works,
        table_name='df_books',
        logger=logger
    )

    # Work keys are stored denormalized (i.e. OLxxxxW)
    df_books['works'] = df_books.works.apply(
        lambda x: KeyHandler.get_key(x[0]['key'])
    )

    # Remove 'works' column
    df_books.rename(columns={'works': 'work_key'}, inplace=True)

    # Filter works not returned from SEARCH
    valid_work_keys = load_json(
        os.path.join(KEYS_DIR, 'romance_fiction_work_keys.json')
    )
    df_books = df_books[df_books.work_key.isin(valid_work_keys)]

    # Separate for each of the final editions tables fields and data
    # Column names to keep for each of the final tables
    editions_fields = [
        'edition_key',  # 'key', # edition key
        "work_key",  # contains work key -> normalize
        "title",
        "subtitle",
        "edition_name",
    ]

    contributors_fields = [
        'edition_key',  # 'key'
        "contributors",
        "by_statement",
        "translated_from",
        "translation_of",
    ]

    publishing_fields = [
        'edition_key',  # 'key'
        "publish_date",
        "publishers",
        "publish_places",
        "publish_country",
        "series",  # name not key
    ]

    content_fields = [
        'edition_key',  # 'key'
        "description",
        "notes",
        "first_sentence",
    ]

    details_fields = [
        'edition_key',  # 'key'
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

    return [
        editions_table,
        contributors_table,
        publishing_table,
        contents_table,
        details_table
    ]

def editions_table(editions_df: pd.DataFrame) -> None:
    """
    Function for saving to csv the 'editions' table
    :param editions_df: pd.DataFrame, containing the editions data as returned from import_editions_data
    """
    # ------------------------------------------------------------------------------
    # --- Editions Table ---

    # Set data types for each column
    # editions_dtypes = {
    #     'edition_key': 'string',
    #     "work_key": 'string',
    #     "title": 'string',
    #     "subtitle": 'string',
    #     "edition_name": 'string',
    # }

    # Prepare tables for exporting
    editions_df = prepare_table(
        editions_df,
        dtypes=editions_dtypes,
        primary_key='edition_key',
        table_name='editions',
        drop_na_except='edition_key',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: 'edition_key'
    save_csv(
        df=editions_df,
        filename='editions.csv',
        directory=CSV_DIR
    )
    # ------------------------------------------------------------------------------

def editions_contributors_table(contributors_df: pd.DataFrame) -> None:
    """
    Function for saving to csv the 'editions_contributors' table
    :param contributors_df: pd.DataFrame, containing the contributors data as returned from import_editions_data
    """
    # ------------------------------------------------------------------------------
    # --- Contributors Table ---

    # Check if any row in 'contributors' has more than one contributor -> Answer: True
    check_explode(
        col=contributors_df.contributors,
        table_name='contributors',
        logger=logger
    )

    # 'contributors' is exploded as to have one contributor per row for some editions
    contributors_df = contributors_df.explode(column='contributors')

    # Extract contributor name and role to two separate columns
    contributors_df[['contributor_name', 'contributor_role']] = contributors_df.contributors.apply(
        lambda x: pd.Series([x['name'], x['role']])
        if isinstance(x, dict) and 'name' in x.keys() and 'role' in x.keys()
        else pd.Series([np.nan, np.nan])
    )

    # Drop 'contributors' column from table
    contributors_df.drop('contributors', inplace=True, axis=1)

    # Check if any row in 'translated_from' has more than one contributor -> Answer: False
    check_explode(
        col=contributors_df.translated_from,
        table_name='translated_from',
        logger=logger
    )

    # Extract the language from 'translated_from'
    contributors_df['translated_from'] = contributors_df.translated_from.apply(
        lambda x: get_language(x[0]['key'])
        if isinstance(x, list)
        else np.nan
    )

    # Reorder columns
    contributors_df = contributors_df[
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
    # contributors_dtypes = {
    #     'edition_key': 'string',
    #     "contributor_name": 'string',
    #     "contributor_role": 'string',
    #     "by_statement": 'string',
    #     "translation_of": 'string',
    #     "translated_from": 'string',
    # }

    # Prepare tables for exporting
    contributors_df = prepare_table(
        contributors_df,
        dtypes=contributors_dtypes,
        primary_key=None,
        table_name='contributors',
        drop_na_except='edition_key',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: None
    save_csv(
        df=contributors_df,
        filename='editions_contributors.csv',
        directory=CSV_DIR
    )
    # ------------------------------------------------------------------------------

def editions_publishing_table(publishing_df: pd.DataFrame) -> None:
    """
    Function for saving to csv the 'editions_publishing' table
    :param publishing_df: pd.DataFrame, containing the publishing data as returned from import_editions_data
    """
    # ------------------------------------------------------------------------------
    # --- Publishing Table ---

    # Extract the publishing year form publish_date
    publishing_df['publish_year'] = publishing_df.publish_date.apply(find_year)

    # Check if more than one publisher name is referred to an edition -> Answer: TRUE
    check_explode(
        col=publishing_df.publishers,
        table_name='publishing',
        logger=logger
    )

    # 'publishers' is exploded as to have one publisher per row for some editions
    publishing_df = publishing_df.explode('publishers')

    # Rename 'publishers'
    publishing_df.rename(columns={'publishers': 'publisher'}, inplace=True)

    # Check if more than one publish_places name is referred to an edition -> Answer: TRUE
    check_explode(
        col=publishing_df.publish_places,
        table_name='publish_places',
        logger=logger
    )

    # 'publish_places' is exploded as to have one publish place per row for some editions
    publishing_df = publishing_df.explode('publish_places')

    # Rename 'publish_places'
    publishing_df.rename(columns={'publish_places': 'publish_place'}, inplace=True)

    # Check if more than one publish_places name is referred to an edition -> Answer: TRUE
    check_explode(
        col=publishing_df.series,
        table_name='series',
        logger=logger
    )

    # 'publish_places' is exploded as to have one publish place per row for some editions
    publishing_df = publishing_df.explode('series')

    # Reorder columns
    publishing_df = publishing_df[
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
    # publishing_dtypes = {
    #     'edition_key': 'string',
    #     "publish_date": 'string',
    #     "publisher": 'string',
    #     "publish_place": 'string',
    #     "publish_country": 'string',
    #     "series": 'string',
    #     "publish_year": "Int64"
    # }

    # Prepare tables for exporting
    publishing_df = prepare_table(
        publishing_df,
        dtypes=publishing_dtypes,
        primary_key=None,
        table_name='publishing',
        drop_na_except='edition_key',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: 'edition_key'
    save_csv(
        df=publishing_df,
        filename='editions_publishing.csv',
        directory=CSV_DIR
    )
    # ------------------------------------------------------------------------------

def editions_contents_table(contents_df: pd.DataFrame) -> None:
    """
    Function for saving to csv the 'editions_contents' table
    :param contents_df: pd.DataFrame, containing the content data as returned from import_editions_data
    """
    # ------------------------------------------------------------------------------
    # --- Contents Table ---

    # Extract description
    contents_df['description'] = contents_df.description.apply(extract_text)

    # Extract notes
    contents_df['notes'] = contents_df.notes.apply(extract_text)

    # Extract first sentence
    contents_df['first_sentence'] = contents_df.first_sentence.apply(extract_text)

    # Set data types for each column
    # contents_dtypes = {
    #     'edition_key': 'string',
    #     "description": 'string',
    #     "notes": 'string',
    #     "first_sentence": 'string',
    # }

    # Prepare tables for exporting
    contents_df = prepare_table(
        contents_df,
        dtypes=contents_dtypes,
        primary_key='edition_key',
        table_name='contents',
        drop_na_except='edition_key',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: 'edition_key'
    save_csv(
        df=contents_df,
        filename='editions_contents.csv',
        directory=CSV_DIR
    )
    # ------------------------------------------------------------------------------

def editions_details_table(details_df: pd.DataFrame) -> None:
    """
    Function for saving to csv the 'editions_details' table
    :param details_df: pd.DataFrame, containing the details data as returned from import_editions_data
    """
    # ------------------------------------------------------------------------------
    # --- Editions Details Table ---

    # Check if more than one language referred to an edition -> Answer: FALSE
    check_explode(
        col=details_df.languages,
        table_name='details',
        logger=logger
    )

    # 'languages' is exploded as to have one language per row for some editions
    details_df = details_df.explode('languages')

    # Extract languages
    details_df['languages'] = details_df.languages.apply(
        lambda x: get_language(x['key'])
        if isinstance(x, dict) and 'key' in x.keys()
        else np.nan
    )

    # Rename 'languages' column
    details_df.rename(columns={'languages': 'language'}, inplace=True)

    # Set data types for each column
    # details_dtypes = {
    #     'edition_key': 'string',
    #     "number_of_pages": 'Int64',
    #     "physical_format": 'string',
    #     "physical_dimensions": 'string',
    #     "weight": 'string',
    #     "language": 'string',
    # }

    # Prepare tables for exporting
    details_df = prepare_table(
        details_df,
        dtypes=details_dtypes,
        # primary_key='edition_key',
        table_name='details',
        drop_na_except='edition_key',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: 'edition_key'
    save_csv(
        df=details_df,
        filename='editions_details.csv',
        directory=CSV_DIR
    )
    # ------------------------------------------------------------------------------

def run() -> None:
    editions, contributors, publishing, contents, details = import_editions_data()
    editions_table(editions)
    editions_contributors_table(contributors)
    editions_publishing_table(publishing)
    editions_contents_table(contents)
    editions_details_table(details)
