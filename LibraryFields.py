"""
Contains the fields that will be used, classified
"""

FIELDS = [
    # Identity
    "key",
    # "ia", # Internet Archive ID

    # Work
    "title",
    "subtitle",
    "alternative_title",
    "alternative_subtitle",
    "first_publish_year",

    # Edition
    "edition_key",
    "format",

    # Editions
    "edition_count",
    "number_of_pages_median",
    "publish_date",
    "publish_year",
    "language",
    "isbn",

    # Series
    "series_key",
    "series_name",
    "series_position",

    # Author
    "author_key",
    "author_name",
    "author_facet", # A normalized version of author names used for filtering
    "author_alternative_name",
    "contributor",

    # Publisher
    "publisher",
    "publisher_facet", # A normalized version of publisher names used for filtering
    "publish_place",

    # Content metadata
    "subject", "subject_key",
    "person", "person_key",
    "place", "place_key",
    "time", "time_key",

    # Accessibility
    "ebook_access",
    "has_fulltext",
    "ia_count", # number of Internet Archive items associated with that work
    "public_scan_b", # at least one publicly available scanned copy in the Internet Archive

    # Statistics
    "ratings_count", # Number of ratings
    "readinglog_count", # Total reading log entries
    "want_to_read_count", # Users who want to read it
    "currently_reading_count", # Users currently reading it
    "already_read_count", # Users who finished it

]

SEARCH_FIELDS_CLASSIFIED = {
    'identity': [
        'key'  # General work key
    ],

    'work': [
        'title',
        'subtitle',
        'first_publish_year'
    ],

    'editions_general': [
        'edition_count',
        'language'
    ],

    'series': [
        'series_key',
        'series_name',
        'series_position'
    ],

    'author': [
        'author_key',
        'author_name'
    ],

    'accessibility': [
        'ebook_access',
        'has_fulltext',
        'public_scan_b'  # at least one publicly available scanned copy in the Internet Archive
    ]
}

SEARCH_FIELDS = {
    'key',
    'title',
    'subtitle',
    'first_publish_year',
    'edition_count',
    'language',
    'series_key',
    'series_name',
    'series_position',
    'author_key',
    'author_name',
    'ebook_access',
    'has_fulltext',
    'public_scan_b'
}