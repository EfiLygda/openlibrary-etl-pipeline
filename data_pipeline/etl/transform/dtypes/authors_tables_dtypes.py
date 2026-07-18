"""
Contains schemas for each authors table and their respective original field from the API

See etl/extract/docs/entrypoints.md for 'SEARCH', 'AUTHORS', 'SEARCH_AUTHORS', 'BOOKS' and 'WORKS'
"""

# ------------------------------------------------------------------------------
# Authors' Tables
# ------------------------------------------------------------------------------

authors_dtypes = {
    'author_key': 'string',                 # FROM: SEARCH.author_key
    'author_name': 'string',                # FROM: SEARCH.author_name | AUTHORS.name | AUTHORS.personal_name
    'bio': 'string',                        # FROM: AUTHORS.bio.value
    'birth_date': 'string',                 # FROM: AUTHORS.birth_date
    'death_date': 'string',                 # FROM: AUTHORS.death_date
    'birth_year': 'Int64',                  # FROM: extracted from 'birth_date'
    'death_year': 'Int64'                   # FROM: extracted from 'death_date'
}

authors_alternative_names_dtypes = {
    'author_key': 'string',                 # FROM: SEARCH.author_key
    'author_alternative_name': 'string',    # FROM: AUTHORS.alternate_names
}

author_statistics_dtypes = {
    'author_key': 'string',                 # FROM: SEARCH.author_key
    'top_work': 'string',                   # FROM: SEARCH_AUTHORS.top_work
    'work_count': 'Int64',                  # FROM: SEARCH_AUTHORS.work_count
    'ratings_count_1': 'Int64',             # FROM: SEARCH_AUTHORS.ratings_count_1
    'ratings_count_2': 'Int64',             # FROM: SEARCH_AUTHORS.ratings_count_2
    'ratings_count_3': 'Int64',             # FROM: SEARCH_AUTHORS.ratings_count_3
    'ratings_count_4': 'Int64',             # FROM: SEARCH_AUTHORS.ratings_count_4
    'ratings_count_5': 'Int64',             # FROM: SEARCH_AUTHORS.ratings_count_5
    'readinglog_count': 'Int64',            # FROM: SEARCH_AUTHORS.readinglog_count
    'want_to_read_count': 'Int64',          # FROM: SEARCH_AUTHORS.want_to_read_count
    'currently_reading_count': 'Int64',     # FROM: SEARCH_AUTHORS.currently_reading_count
    'already_read_count': 'Int64',          # FROM: SEARCH_AUTHORS.already_read_count
}

authors_works_dtypes = {
    'work_key': 'string',                   # FROM: SEARCH.key
    'author_key': 'string',                 # FROM: SEARCH.author_key
}
# ------------------------------------------------------------------------------
