SELECT
    author_key,

    top_work,
    work_count,

    ratings_count_1,
    ratings_count_2,
    ratings_count_3,
    ratings_count_4,
    ratings_count_5,

    readinglog_count,
    want_to_read_count,
    currently_reading_count,
    already_read_count
FROM
    authors_statistics
WHERE
    author_key = %(filter_key)s
