import os
import pandas as pd
from config import AUTHORS_DIR
from utilities import find_year
from open_library import JSONFileHandler, KeyHandler


author_files = [
    os.path.join(AUTHORS_DIR, filename)
    for filename in os.listdir(AUTHORS_DIR)
]

all_records = dict()

for filename in author_files:
    data = JSONFileHandler.load_json(filename)
    all_records.update(data['result'])

df = pd.DataFrame(all_records).T
df.rename(columns={'name': 'author_name'}, inplace=True)

new_index = [KeyHandler.get_key(i) for i in df.index]

df.index = new_index

df.reset_index(inplace=True, names='author_key')

# ---------------------------------------------
# 1. AUTHORS_TABLE
authors_table_columns_to_keep = [
    'author_key',
    'author_name',
    'bio',
    'birth_date',
    'death_date',
]

authors_table = df[authors_table_columns_to_keep]

authors_table['birth_year'] = df.birth_date.apply(find_year)
authors_table['death_year'] = df.death_date.apply(find_year)
# ---------------------

# ---------------------
# AUTHORS_ALTERNATIVE_NAMES_TABLE
authors_alternative_names_table = df[['author_key', 'alternate_names']].explode('alternate_names')
# ---------------------
