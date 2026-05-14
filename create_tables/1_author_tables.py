import os
import numpy as np
import pandas as pd
from config import AUTHORS_DIR, AUTHORS_STATISTICS_DIR, GENRE_facet, KEYS_DIR, WORKS_DIR
from utilities import find_year
from open_library import JSONFileHandler, KeyHandler


author_files = [
    os.path.join(AUTHORS_DIR, filename)
    for filename in os.listdir(AUTHORS_DIR)
]

all_author_records = dict()

for filename in author_files:
    data = JSONFileHandler.load_json(filename)
    all_author_records.update(data['result'])

df_authors = pd.DataFrame(all_author_records).T
df_authors.rename(columns={'name': 'author_name'}, inplace=True)

new_index = [KeyHandler.get_key(i) for i in df_authors.index]
df_authors.index = new_index

df_authors.reset_index(inplace=True, names='author_key')

# ---------------------------------------------
# 1. AUTHORS_TABLE
authors_table_columns_to_keep = [
    'author_key',
    'author_name',
    'bio',
    'birth_date',
    'death_date',
]

authors_table = df_authors[authors_table_columns_to_keep]

authors_table['birth_year'] = df_authors.birth_date.apply(find_year)
authors_table['death_year'] = df_authors.death_date.apply(find_year)
# ---------------------

# ---------------------
# AUTHORS_ALTERNATIVE_NAMES_TABLE
authors_alternative_names_table = df_authors[['author_key', 'alternate_names']].explode('alternate_names')
# ---------------------

# ---------------------
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
# ---------------------

# ---------------------
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
# ---------------------


