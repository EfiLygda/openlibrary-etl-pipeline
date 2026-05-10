"""
Contains the fields that will be used, classified by query used
"""

# --- General Work ---
SEARCH_FIELDS = {
    'key',                  # str       |   Work key
    'title',                # str       |   Work title
    'subtitle',             # str       |   Work subtitle
    'edition_count',        # int       |   Work no of editions
    'series_key',           # list[str] |   Work series key
    'series_name',          # list[str] |   Work series name
    'series_position',      # list[str] |   Work series position
    'author_key',           # list[str] |   Work author key
    'author_name',          # list[str] |   Work author name
    'ebook_access',         # str       |   Work type of ebook access
    'has_fulltext'          # bool      |   Whether full text is available for work
}

# --- Specific Work Enriched ---
WORKS_FIELDS = {
    'key',                  # str       |   Work key
    'title',                # str       |   Work title
    'first_publish_date',   # str       |   Work first publish date
    'description',          # str       |   Work description
    'authors',              # list[dict]|   Work authors with names and types of author
                            #           |   author_key : 'authors'[i] -> 'author' -> 'key'
                            #           |   author_type: 'authors'[i] -> 'type' -> 'key'
    'subjects',             # list[str] |   List of subjects in work
    'subject_people',       # list[str] |   List of people in work
    'subject_places',       # list[str] |   List of places in work
    'subject_times'         # list[str] |   List of time periods in work
}

# --- Specific Editions ---
BOOKS_FIELDS = {
    'key',                  # str       |   Edition key
    'subtitle',             # str       |   Edition subtitle
    'contributors',         # list[dict]|   Work contributors
                            #           |   contributor_name: contributors[i] -> name
                            #           |   contributor_role: contributors[i] -> role
    'number_of_pages',      # int       |   Number of pages in edition
    'physical_format',      # str       |   Type of physical format of the edition
    'publish_date',         # str       |   Date of publication for the edition
    'publish_places',       # list[str] |   List of publication's places for the edition
    'publishers',           # list[str] |   List of publishers' names
    'languages',            # list[dict]|   Edition's languages
                            #           |   language: languages[i] -> key
    'isbn_10',              # list[str] |   List of ISBN-10 (only one value)
    'isbn_13',              # list[str] |   List of ISBN-13 (only one value)
}

# --- Authors ---
AUTHORS_FIELDS = {
    'key',                  # str       |   Author key
    'name',                 # str       |   Author name
    'personal_name',        # str       |   Author name (TODO: check differences with 'name')
    'alternate_names',      # list[str] |   List of author's alternative names
    'bio'                   # dict      |   Author's bio
                            #           |   bio: bio -> value
}

# --- Authors Enriched ---
SEARCH_AUTHORS_FIELDS = {
    'key',                      # str   |   Author key
    'top_work',                 # str   |   Author's top work
    'ratings_count_1',          # int   |   Author's number of one-star ratings
    'ratings_count_2',          # int   |   Author's number of two-star ratings
    'ratings_count_3',          # int   |   Author's number of three-star ratings
    'ratings_count_4',          # int   |   Author's number of four-star ratings
    'ratings_count_5',          # int   |   Author's number of five-star ratings
    'readinglog_count',         # int   |   Author's total reading log entries
    'want_to_read_count',       # int   |   Author's users who want to read it
    'currently_reading_count',  # int   |   Author's users currently reading it
    'already_read_count',       # int   |   Author's users who finished it

}

# --- Publishers ---
PUBLISHERS_FIELDS = {
    'key',              # str       | Publisher's key
    'name',             # str       | Publisher's name
    'work_count',       # int       | Number of works under the publisher
}

# --- Subjects ---
SUBJECTS_FIELDS = {
    'key',              # str       | Subjects's key
    'name',             # str       | Subjects's name
    'work_count',       # int       | Number of works under the subject
}

# --- Subjects ---
PERSONS_FIELDS = {
    'key',              # str       | Person's key
    'name',             # str       | Person's name
    'work_count',       # int       | Number of works under the person
}