"""
Contains the field names for each table in the schema
"""

# NOTE: SEARCH_EDITIONS_VIA_WORK_KEY can be used for batch searching BOOKS (see STEP 4)
# TODO: IMPORTANT!!!
#  ADD in OpenLibraryClient a way to use the SEARCH_AUTHORS and SEARCH_EDITIONS_VIA_WORK_KEY query

# --- A. Strategy for Extraction of Data ---
# STEP 1: Extract all works under the genre via SEARCH (DONE)
# STEP 2: Extract all work keys, author keys, series keys, (DONE)
# STEP 3: Use OpenLibraryClient.get_many to extract via keys all WORKS, AUTHORS, SERIES

# STEP 4: Use SEARCH_EDITIONS_VIA_WORK_KEY to find all editions in a work
# STEP 5: Use SEARCH_EDITIONS_VIA_WORK_KEY.entries[i].key to extract all BOOKS fields

# Step 6: Extract all publisher names via SEARCH_EDITIONS_VIA_WORK_KEY.entries[i].publishers
# Step 7: Use OpenLibraryClient.get_publisher to extract all PUBLISHERS fields

# Step 8: Extract all SUBJECTS from SEARCH_EDITIONS_VIA_WORK_KEY.entries[i].subjects
# Step 9: Extract all SUBJECTS from SEARCH_EDITIONS_VIA_WORK_KEY.entries[i].subject_people
# Step 10: Extract all SUBJECTS from SEARCH_EDITIONS_VIA_WORK_KEY.entries[i].subject_times
# Step 11: Use OpenLibraryClient.get to extract all SUBJECTS, PERSONS, TIMES fields

# Step 12: Extract all SEARCH_AUTHORS fields from SEARCH_AUTHORS


WORKS_TABLE = {
    'work_key',             # FROM: SEARCH.key
    'title',                # FROM: SEARCH.title
    'subtitle',             # FROM: SEARCH.subtitle
    'first_publish_date',   # FROM: WORKS.first_publish_date
    'edition_count',        # FROM: SEARCH.edition_count
    'description',          # FROM: WORKS.description
    'ebook_access',         # FROM: SEARCH.ebook_access
    'has_fulltext'          # FROM: SEARCH.has_fulltext
}

AUTHORS_TABLE = {
    'author_key',           # FROM: SEARCH.author_key
    'author_name',          # FROM: SEARCH.author_name | AUTHORS.name | AUTHORS.personal_name
    'bio',                  # FROM: AUTHORS.bio.value
}

EDITIONS_TABLE = {
  'edition_key',            # FROM: BOOKS.key | SEARCH_EDITIONS_VIA_WORK_KEY.entries[i].key
  'work_key',               # FROM: SEARCH.key
  'physical_format',        # FROM: BOOKS.physical_format
  'publisher_name',         # FROM: BOOKS.publisher_name | PUBLISHERS.name
  'publish_date',           # FROM: BOOKS.publish_date
  'language',               # FROM: BOOKS.languages
  'isbn_10',                # FROM: BOOKS.isbn_10
  'isbn_13',                # FROM: BOOKS.isbn_13
}

SERIES_TABLE = {
  'series_key',             # FROM: SEARCH.series_key
  'series_name',            # FROM: SEARCH.series_name
}

PUBLISHERS_TABLE = {
  'publisher_name',         # FROM: BOOKS.publishers | PUBLISHERS.name
  'work_count',             # FROM: PUBLISHERS.work_count
}

SUBJECTS_TABLE = {
  'subject_key',            # FROM: SUBJECTS.key
  'subject',                # FROM: WORKS.subjects
  'work_count',             # FROM: SUBJECTS.work_count
}

PERSONS_TABLE = {
  'person_key',             # FROM: PERSONS.key
  'person',                 # FROM: WORKS.subject_people | PERSONS.name
  'work_count',             # FROM: PERSONS.work_count
}

WORKS_AUTHORS_TABLE = {
  'work_key',               # FROM: SEARCH.key
  'author_key'              # FROM: SEARCH.author_key
}

WORKS_SUBJECTS_TABLE = {
  'work_key',               # FROM: SEARCH.key
  'subject_key'             # FROM: SUBJECTS.key
}

WORKS_PERSONS_TABLE = {
  'work_key',               # FROM: SEARCH.key
  'person_key',             # FROM: PERSONS.key
}

WORKS_PLACES_TABLE = {
  'work_key',               # FROM: SEARCH.key
  'place',                  # FROM: WORKS.subject_places
}

WORKS_TIMES_TABLE = {
  'work_key',               # FROM: SEARCH.key
  'time',                   # FROM: WORKS.subject_times
}

WORKS_SERIES_TABLE = {
  'work_key',               # FROM: SEARCH.key
  'series_key',             # FROM: SEARCH.series_key
  'series_position',        # FROM: SEARCH.series_position
}

AUTHORS_STATISTICS_TABLE = {
  'author_key',             # FROM: SEARCH.author_key
  'ratings_count_1',        # FROM: SEARCH_AUTHORS.ratings_count_1
  'ratings_count_2',        # FROM: SEARCH_AUTHORS.ratings_count_2
  'ratings_count_3',        # FROM: SEARCH_AUTHORS.ratings_count_3
  'ratings_count_4',        # FROM: SEARCH_AUTHORS.ratings_count_4
  'ratings_count_5',        # FROM: SEARCH_AUTHORS.ratings_count_5
  'readinglog_count',       # FROM: SEARCH_AUTHORS.readinglog_count
  'want_to_read_count',     # FROM: SEARCH_AUTHORS.want_to_read_count
  'currently_reading_count',# FROM: SEARCH_AUTHORS.currently_reading_count
  'already_read_count',     # FROM: SEARCH_AUTHORS.already_read_count
}

AUTHORS_ALTERNATIVE_NAMES_TABLE = {
  'author_key',             # FROM: SEARCH.author_key
  'author_alternative_name',# FROM: AUTHORS.alternate_names
}

EDITIONS_CONTRIBUTORS_TABLE = {
  'edition_key',            # FROM: BOOKS.key
  'contributor_name',       # FROM: BOOKS.contributors.name
  'contributor_role',       # FROM: BOOKS.contributors.role
}