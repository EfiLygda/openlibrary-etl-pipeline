"""
Contains dtypes for each editions table and their respective original field from the API

See /API_info/base_urls for 'SEARCH', 'AUTHORS', 'SEARCH_AUTHORS', 'BOOKS' and 'WORKS'
"""

# ------------------------------------------------------------------------------
# Editions' Tables
# ------------------------------------------------------------------------------

editions_dtypes = {
    'edition_key': 'string',            # FROM: BOOKS.key | SEARCH_EDITIONS_VIA_WORK_KEY.entries[i].key
    "work_key": 'string',               # FROM: SEARCH.key
    "title": 'string',                  # FROM: BOOKS.title
    "subtitle": 'string',               # FROM: BOOKS.title
    "edition_name": 'string',           # FROM: BOOKS.edition_name
}

contributors_dtypes = {
    'edition_key': 'string',            # FROM: BOOKS.key
    "contributor_name": 'string',       # FROM: BOOKS.contributors.name
    "contributor_role": 'string',       # FROM: BOOKS.contributors.role
    "by_statement": 'string',           # FROM: BOOKS.by_statement
    "translation_of": 'string',         # FROM: BOOKS.translation_of
    "translated_from": 'string',        # FROM: BOOKS.translated_from.key
}

publishing_dtypes = {
    'edition_key': 'string',            # FROM: BOOKS.key
    "publish_date": 'string',           # FROM: BOOKS.publish_date
    "publisher": 'string',              # FROM: BOOKS.publisher_name | PUBLISHERS.name
    "publish_place": 'string',          # FROM: BOOKS.publish_places[i]
    "publish_country": 'string',        # FROM: BOOKS.publish_country
    "series": 'string',                 # FROM: BOOKS.series[i]
    "publish_year": "Int64"             # FROM: extracted from 'publish_date'
}

contents_dtypes = {
    'edition_key': 'string',            # FROM: BOOKS.key
    "description": 'string',            # FROM: BOOKS.description
    "notes": 'string',                  # FROM: BOOKS.notes.value
    "first_sentence": 'string',         # FROM: BOOKS.notes.first_sentence
}

details_dtypes = {
    'edition_key': 'string',            # FROM: BOOKS.key
    "number_of_pages": 'Int64',         # FROM: BOOKS.number_of_pages
    "physical_format": 'string',        # FROM: BOOKS.physical_format
    "physical_dimensions": 'string',    # FROM: BOOKS.physical_dimensions
    "weight": 'string',                 # FROM: BOOKS.weight
    "language": 'string',               # FROM: BOOKS.languages
}
# ------------------------------------------------------------------------------
