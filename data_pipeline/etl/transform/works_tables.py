"""
STEP 3: Create tables `works`, `works_series`, `works_availability`, `works_subjects`,
 `works_people`, `works_places`  and `works_time_periods` tables
"""

import os
import numpy as np
import pandas as pd

from data_pipeline.open_library import KeyHandler

from config.paths import CSV_DIR, WORKS_DIR, SEARCH_DIR, SERIES_DIR, WORKS_RATINGS_DIR

from utilities.io import load_json, save_csv
from data_pipeline.utils.data.parsing import extract_text
from data_pipeline.utils.data.validation import check_explode
from data_pipeline.etl.transform.dtypes import (works_dtypes,
                                                ratings_dtypes,
                                                series_dtypes,
                                                availability_dtypes,
                                                subjects_dtypes,
                                                people_dtypes,
                                                places_dtypes,
                                                times_dtypes)
from data_pipeline.utils.data.table_prep import prepare_table
from utilities.logging import set_logger

logger = set_logger('TRANSFORM_TO_WORKS_TABLES')

def import_works_data() -> list[pd.DataFrame]:
    """
    Function for importing all general works' data and splitting them to 7 dataframes:

    1. works_table,
    2. works_ratings_table,
    3. series_table,
    4. availability_table,
    5. subjects_table,
    6. people_table,
    7. places_table,
    8. times_table

    :return: list[pd.DataFrame], list with the 7 dataframes
    """
    # ------------------------------------------------------------------------------
    # --- Import and convert to dictionaries all works and enriched works' data ---

    # Fetching all works, works enriched and ratings JSON filenames
    works_files = [
        os.path.join(SEARCH_DIR, filename)
        for filename in os.listdir(SEARCH_DIR)
    ]

    works_enriched_files = [
        os.path.join(WORKS_DIR, filename)
        for filename in os.listdir(WORKS_DIR)
    ]

    works_ratings_files = [
        os.path.join(WORKS_RATINGS_DIR, filename)
        for filename in os.listdir(WORKS_RATINGS_DIR)
    ]

    # Dictionaries that will contain all works' data
    # Keys: works keys (i.e. '/books/OLxxxxW')
    # Values: a work's record as returned via an SEARCH query
    all_works_records = dict()

    # For each file all works' data are loaded and updated in the dictionary
    for filename in works_files:

        # Load JSON books' data
        data = load_json(filename)

        for record in data['docs']:
            if record['key'] in all_works_records.keys():
                logger.warning(f'WORK_DUPLICATE_FOUND work_key={record["key"]}')
            else:
                all_works_records[record['key']] = record

    # Keys: works keys (i.e. '/books/OLxxxxW')
    # Values: a work's record as returned via an WORKS query
    all_works_enriched_records = dict()

    # For each file all enriched works' data are loaded and updated in the dictionary
    for filename in works_enriched_files:
        # Load JSON books' data
        data = load_json(filename)

        # Update the dictionary
        all_works_enriched_records.update(data['result'])

    # Keys: works keys (i.e. '/books/OLxxxxW')
    # Values: a work's record as returned via a WORKS_RATINGS query
    all_works_ratings_records = dict()

    # For each file all enriched works' ratings are loaded and updated in the dictionary
    for filename in works_ratings_files:
        # Load JSON books' data
        data = load_json(filename)

        # Update the dictionary
        all_works_ratings_records.update(data)
    # ------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # --- Convert dictionaries to dataframes and merge ---

    # Convert the works' data dictionary to a dataframe and transpose in order
    # to have the author keys as index
    # Notes:
    # 1. the current index has values as '/works/OLxxxxW' -> the keys are going to be denormalized
    # 2. column 'key' also contains each work's keys
    df_works = pd.DataFrame(all_works_records).T
    df_works_enriched = pd.DataFrame(all_works_enriched_records).T

    # Reset index and name it 'key'
    df_works_ratings = pd.DataFrame(all_works_ratings_records).T
    df_works_ratings.reset_index(inplace=True, names='key')

    # Join the three dataframes on the 'key' column
    df_works_all = df_works.merge(df_works_enriched, how='left', on='key', suffixes=('', '__enriched'))
    df_works_all = df_works_all.merge(df_works_ratings, how='left', on='key')
    # ------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # --- Change column names and drop columns ---

    # Rename works 'key' to 'work_key'
    df_works_all.rename(columns={'key': 'work_key'}, inplace=True)

    # Denormalize 'work_key'
    df_works_all['work_key'] = df_works_all.work_key.apply(KeyHandler.get_key)

    # Check if 'title' == 'title__enriched' and 'subtitle' == 'subtitle__enriched' -> Answer: TRUE
    if (df_works_all.title == df_works_all.title__enriched).all():
        logger.warning('REDUNDANT_COLUMN_DROPPED column=title__enriched duplicate_of=title')
        df_works_all.drop('title__enriched', inplace=True, axis=1)

    if (df_works_all.dropna().subtitle == df_works_all.dropna().subtitle__enriched).all():
        logger.warning('REDUNDANT_COLUMN_DROPPED column=subtitle__enriched duplicate_of=subtitle')
        df_works_all.drop('subtitle__enriched', inplace=True, axis=1)
    # ------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # --- Separate to different tables ---

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

    ratings_fields = [
        'work_key',
        '1',
        '2',
        '3',
        '4',
        '5'
    ]

    series_fields = [
        'work_key',
        'series_key',
        'series_position',  # add series name
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

    # Keep only wanted columns for each table
    works_table = df_works_all[works_fields]
    works_ratings_table = df_works_all[ratings_fields]
    series_table = df_works_all[series_fields]
    availability_table = df_works_all[availability_fields]
    subjects_table = df_works_all[subjects_fields]
    people_table = df_works_all[people_fields]
    places_table = df_works_all[places_fields]
    times_table = df_works_all[times_fields]

    return [
        works_table,
        works_ratings_table,
        series_table,
        availability_table,
        subjects_table,
        people_table,
        places_table,
        times_table
    ]

def works_table(works_df: pd.DataFrame) -> None:
    """
    Function for saving to csv the 'works' table
    :param works_df: pd.DataFrame, containing the works data as returned from import_works_data
    """
    # ------------------------------------------------------------------------------
    # --- Works Table ---

    # Extract 'description' text
    works_df['description'] = works_df.description.apply(extract_text)

    # Extract 'first_sentence' text
    works_df['first_sentence'] = works_df.first_sentence.apply(extract_text)

    # Set data types for each column
    # works_dtypes = {
    #     'work_key': 'string',
    #     "title": 'string',
    #     "subtitle": 'string',
    #     "description": 'string',
    #     "first_sentence": 'string',
    #     "edition_count": 'Int64',
    #     "first_publish_year": 'Int64',
    #     "first_publish_date": 'string',
    # }

    # Prepare tables for exporting
    works_df = prepare_table(
        works_df,
        dtypes=works_dtypes,
        primary_key='work_key',
        table_name='works',
        # drop_na_except = 'work_key',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: 'work_key'
    save_csv(
        df=works_df,
        filename='works.csv',
        directory=CSV_DIR
    )
    # ------------------------------------------------------------------------------

def works_ratings_table(works_ratings_df: pd.DataFrame) -> None:
    """
    Function for saving to csv the 'works_ratings' table
    :param works_ratings_df: pd.DataFrame, containing the works data as returned from import_works_data
    """

    # ------------------------------------------------------------------------------
    # --- Works Ratings Table ---
    works_ratings_df.rename(
        columns={
            "1": 'ratings_count_1',
            "2": 'ratings_count_2',
            "3": 'ratings_count_3',
            "4": 'ratings_count_4',
            "5": 'ratings_count_5',
        },
        inplace=True
    )

    # Prepare tables for exporting
    works_ratings_df = prepare_table(
        works_ratings_df,
        dtypes=ratings_dtypes,
        primary_key='work_key',
        table_name='works_ratings',
        drop_na_except = 'work_key',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: 'work_key'
    save_csv(
        df=works_ratings_df,
        filename='works_ratings.csv',
        directory=CSV_DIR
    )

def import_series_data() -> pd.DataFrame:
    """
    Function for importing series data and converting to dataframe
    :return: pd.DataFrame, the dataframe
    """
    # ------------------------------------------------------------------------------
    # --- Import and convert to dictionaries series data ---

    # Fetching all series JSON filenames
    series_files = [
        os.path.join(SERIES_DIR, filename)
        for filename in os.listdir(SERIES_DIR)
    ]

    # Keys: series keys (i.e. '/books/OLxxxxL')
    # Values: a series' record as returned via an WORKS query
    all_series_records = dict()

    # For each file all enriched series' data are loaded and updated in the dictionary
    for filename in series_files:
        # Load JSON books' data
        data = load_json(filename)

        # Update the dictionary
        all_series_records.update(data['result'])
    # ------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # --- Convert dictionaries to dataframes and merge ---

    # Convert the series' data dictionary to a dataframe and transpose in order
    df_series = pd.DataFrame(all_series_records).T
    # ------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------
    # --- Change column names and drop columns ---

    # Reset index and drop the new column
    df_series.reset_index(inplace=True, drop=True)

    # Rename works 'key' to 'series_key'
    df_series.rename(columns={'key': 'series_key'}, inplace=True)

    # Denormalize 'series_key'
    df_series['series_key'] = df_series.series_key.apply(KeyHandler.get_key)

    return df_series

def works_series_table(series_df: pd.DataFrame) -> None:
    """
    Function for saving to csv the 'works_series' table
    :param series_df: pd.DataFrame, containing the series data as returned from import_works_data
    """
    # ------------------------------------------------------------------------------
    # --- Series Table ---

    # Import series data
    df_series = import_series_data()

    # Check if more than one series_key referred to a work -> Answer: FALSE
    check_explode(
        col=series_df.series_key,
        table_name='series',
        logger=logger
    )

    # Extract 'series_key'
    series_df['series_key'] = series_df.series_key.apply(
        lambda x: x[0]
        if isinstance(x, list)
        else np.nan
    )

    # Check if more than one series_position referred to a work -> Answer: FALSE
    check_explode(
        col=series_df.series_position,
        table_name='series',
        logger=logger
    )

    # Extract 'series_key'
    series_df['series_position'] = series_df.series_position.apply(
        lambda x: x[0]
        if isinstance(x, list)
        else np.nan
    )

    # Add series names to the series table
    series_df = series_df.merge(
        df_series[['series_key', 'name']],
        on='series_key',
        how='left'
    )

    # Rename 'name' column to 'series_name'
    series_df.rename(
        columns={
            'name': 'series_name'
        },
        inplace=True
    )

    # Set data types for each column
    # series_dtypes = {
    #     'work_key': 'string',
    #     "series_key": 'string',
    #     "series_position": 'string',
    #     "series_name": 'string',
    # }

    # Prepare tables for exporting
    series_df = prepare_table(
        series_df,
        dtypes=series_dtypes,
        primary_key='work_key',
        table_name='series',
        drop_na_except=['work_key', 'series_key'],
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: 'work_key'
    save_csv(
        df=series_df,
        filename='works_series.csv',
        directory=CSV_DIR
    )
    # ------------------------------------------------------------------------------

def works_availability_table(availability_df: pd.DataFrame) -> None:
    """
    Function for saving to csv the 'works_availability' table
    :param availability_df: pd.DataFrame, containing the availability data as returned from import_works_data
    """
    # ------------------------------------------------------------------------------
    # --- Availability Table ---

    # Rename 'public_scan_b' to 'has_public_scan'
    availability_df.rename(columns={'public_scan_b': 'has_public_scan'}, inplace=True)

    # Set data types for each column
    # availability_dtypes = {
    #     'work_key': 'string',
    #     "ebook_access": 'string',
    #     "has_fulltext": 'bool',
    #     "has_public_scan": 'bool',
    # }

    # Prepare tables for exporting
    availability_df = prepare_table(
        availability_df,
        dtypes=availability_dtypes,
        primary_key='work_key',
        table_name='availability',
        drop_na_except='work_key',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: 'work_key'
    save_csv(
        df=availability_df,
        filename='works_availability.csv',
        directory=CSV_DIR
    )
    # ------------------------------------------------------------------------------

def works_subjects_table(subjects_df: pd.DataFrame) -> None:
    """
    Function for saving to csv the 'works_subjects' table
    :param subjects_df: pd.DataFrame, containing the subjects data as returned from import_works_data
    """
    # ------------------------------------------------------------------------------
    # --- Subjects Table ---

    # Check if more than one 'subjects' referred to a work -> Answer: TRUE
    check_explode(
        col=subjects_df.subjects,
        table_name='subjects',
        logger=logger
    )

    # Explode 'subjects'
    subjects_df = subjects_df.explode(column='subjects')

    # Rename 'subjects' to 'subject'
    subjects_df.rename(columns={'subjects': 'subject'}, inplace=True)

    # Set data types for each column
    # subjects_dtypes = {
    #     'work_key': 'string',
    #     "subject": 'string',
    # }

    # Prepare tables for exporting
    subjects_df = prepare_table(
        subjects_df,
        dtypes=subjects_dtypes,
        primary_key=['work_key', 'subject'],
        table_name='subjects',
        drop_na_except='work_key',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: 'work_key','subject'
    save_csv(
        df=subjects_df,
        filename='works_subjects.csv',
        directory=CSV_DIR
    )
    # ------------------------------------------------------------------------------

def works_people_table(people_df: pd.DataFrame) -> None:
    """
    Function for saving to csv the 'works_people' table
    :param people_df: pd.DataFrame, containing the people data as returned from import_works_data
    """
    # ------------------------------------------------------------------------------
    # --- People Table ---

    # Check if more than one 'subject_people' referred to a work -> Answer: TRUE
    check_explode(
        col=people_df.subject_people,
        table_name='people',
        logger=logger
    )

    # Explode 'subject_people'
    people_df = people_df.explode(column='subject_people')

    # Rename 'subject_people' to 'person'
    people_df.rename(columns={'subject_people': 'person'}, inplace=True)

    # Set data types for each column
    # people_dtypes = {
    #     'work_key': 'string',
    #     "person": 'string',
    # }

    # Prepare tables for exporting
    people_df = prepare_table(
        people_df,
        dtypes=people_dtypes,
        primary_key=['work_key', 'person'],
        table_name='people',
        drop_na_except='work_key',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: 'work_key','person'
    save_csv(
        df=people_df,
        filename='works_people.csv',
        directory=CSV_DIR
    )
    # ------------------------------------------------------------------------------

def works_places_table(places_df: pd.DataFrame) -> None:
    """
    Function for saving to csv the 'works_places' table
    :param places_df: pd.DataFrame, containing the places data as returned from import_works_data
    """
    # ------------------------------------------------------------------------------
    # --- Places Table ---

    # Check if more than one 'subject_places' referred to a work -> Answer: TRUE
    check_explode(
        col=places_df.subject_places,
        table_name='places',
        logger=logger
    )

    # Explode 'subject_places'
    places_df = places_df.explode(column='subject_places')

    # Rename 'subject_places' to 'place'
    places_df.rename(columns={'subject_places': 'place'}, inplace=True)

    # Set data types for each column
    # places_dtypes = {
    #     'work_key': 'string',
    #     "place": 'string',
    # }

    # Prepare tables for exporting
    places_df = prepare_table(
        places_df,
        dtypes=places_dtypes,
        primary_key=['work_key', 'place'],
        table_name='places',
        drop_na_except='work_key',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: 'work_key','person'
    save_csv(
        df=places_df,
        filename='works_places.csv',
        directory=CSV_DIR
    )
    # ------------------------------------------------------------------------------

def works_times_table(times_df: pd.DataFrame) -> None:
    """
    Function for saving to csv the 'works_times' table
    :param times_df: pd.DataFrame, containing the times data as returned from import_works_data
    """
    # ------------------------------------------------------------------------------
    # --- Times Table ---

    # Check if more than one 'subject_times' referred to a work -> Answer: TRUE
    check_explode(
        col=times_df.subject_times,
        table_name='times',
        logger=logger
    )

    # Explode 'subject_times'
    times_df = times_df.explode(column='subject_times')

    # Rename 'subject_times' to 'time_period'
    times_df.rename(columns={'subject_times': 'time_period'}, inplace=True)

    # Set data types for each column
    # times_dtypes = {
    #     'work_key': 'string',
    #     "time_period": 'string',
    # }

    # Prepare tables for exporting
    times_df = prepare_table(
        times_df,
        dtypes=times_dtypes,
        primary_key=['work_key', 'time_period'],
        table_name='times',
        drop_na_except='work_key',
        drop_duplicates=True,
        logger=logger
    )

    # Export table as a CSV file
    # Primary key: 'work_key','time_period'
    save_csv(
        df=times_df,
        filename='works_time_periods.csv',
        directory=CSV_DIR
    )
    # ------------------------------------------------------------------------------

def run():
    works_df, works_ratings_df, series_df, availability_df, subjects_df, people_df, places_df, times_df = import_works_data()
    works_table(works_df)
    works_ratings_table(works_ratings_df)
    works_series_table(series_df)
    works_availability_table(availability_df)
    works_subjects_table(subjects_df)
    works_people_table(people_df)
    works_places_table(places_df)
    works_times_table(times_df)
