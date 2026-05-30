"""
Contains dtypes for each works table and their respective original field from the API

See /API_info/base_urls for 'SEARCH', 'AUTHORS', 'SEARCH_AUTHORS', 'BOOKS' and 'WORKS'
"""

# ------------------------------------------------------------------------------
# Works' Tables
# ------------------------------------------------------------------------------

works_dtypes = {
    'work_key': 'string',               # FROM: SEARCH.key
    "title": 'string',                  # FROM: SEARCH.title
    "subtitle": 'string',               # FROM: SEARCH.subtitle
    "description": 'string',            # FROM: WORKS.description
    "first_sentence": 'string',         # FROM: WORKS.first_sentence.value
    "edition_count": 'Int64',           # FROM: SEARCH.edition_count
    "first_publish_year": 'Int64',      # FROM: SEARCH.first_publish_year
    "first_publish_date": 'string',     # FROM: WORKS.first_publish_date
}

series_dtypes = {
    'work_key': 'string',               # FROM: SEARCH.key
    "series_key": 'string',             # FROM: SEARCH.series_key
    "series_position": 'string',        # FROM: SEARCH.series_position
    "name": 'string',                   # FROM: SEARCH.series_name
}

availability_dtypes = {
    'work_key': 'string',               # FROM: SEARCH.key
    "ebook_access": 'string',           # FROM: SEARCH.ebook_access
    "has_fulltext": 'bool',             # FROM: SEARCH.has_fulltext
    "has_public_scan": 'bool',          # FROM: WORKS.public_scan_b
}

subjects_dtypes = {
    'work_key': 'string',               # FROM: SEARCH.key
    "subject": 'string',                # FROM: WORKS.subjects
}

people_dtypes = {
    'work_key': 'string',               # FROM: SEARCH.key
    "person": 'string',                 # FROM: WORKS.subject_people | PERSONS.name
}

places_dtypes = {
    'work_key': 'string',               # FROM: SEARCH.key
    "place": 'string',                  # FROM: WORKS.subject_places
}

times_dtypes = {
    'work_key': 'string',               # FROM: SEARCH.key
    "time_period": 'string',            # FROM: WORKS.subject_times
}
# ------------------------------------------------------------------------------
