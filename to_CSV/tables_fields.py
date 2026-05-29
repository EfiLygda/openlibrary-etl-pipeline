# ------------------------------------------------------------------------------
# Authors' Tables
# ------------------------------------------------------------------------------

authors_dtypes = {
    'author_key': 'string',
    'author_name': 'string',
    'bio': 'string',
    'birth_date': 'string',
    'death_date': 'string',
    'birth_year': 'Int64',
    'death_year': 'Int64'
}

authors_alternative_names_dtypes = {
    'author_key': 'string',
    'author_alternative_name': 'string',
}

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

authors_works_dtypes = {
    'work_key': 'string',
    'author_key': 'string',
}
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Editions' Tables
# ------------------------------------------------------------------------------

editions_dtypes = {
    'edition_key': 'string',
    "work_key": 'string',
    "title": 'string',
    "subtitle": 'string',
    "edition_name": 'string',
}

contributors_dtypes = {
    'edition_key': 'string',
    "contributor_name": 'string',
    "contributor_role": 'string',
    "by_statement": 'string',
    "translation_of": 'string',
    "translated_from": 'string',
}

publishing_dtypes = {
    'edition_key': 'string',
    "publish_date": 'string',
    "publisher": 'string',
    "publish_place": 'string',
    "publish_country": 'string',
    "series": 'string',
    "publish_year": "Int64"
}

contents_dtypes = {
    'edition_key': 'string',
    "description": 'string',
    "notes": 'string',
    "first_sentence": 'string',
}

details_dtypes = {
    'edition_key': 'string',
    "number_of_pages": 'Int64',
    "physical_format": 'string',
    "physical_dimensions": 'string',
    "weight": 'string',
    "language": 'string',
}
# ------------------------------------------------------------------------------

# ------------------------------------------------------------------------------
# Works' Tables
# ------------------------------------------------------------------------------

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

series_dtypes = {
    'work_key': 'string',
    "series_key": 'string',
    "series_position": 'string',
    "name": 'string',
}

availability_dtypes = {
    'work_key': 'string',
    "ebook_access": 'string',
    "has_fulltext": 'bool',
    "has_public_scan": 'bool',
}

subjects_dtypes = {
    'work_key': 'string',
    "subject": 'string',
}

people_dtypes = {
    'work_key': 'string',
    "person": 'string',
}

places_dtypes = {
    'work_key': 'string',
    "place": 'string',
}

times_dtypes = {
    'work_key': 'string',
    "time_period": 'string',
}
# ------------------------------------------------------------------------------
