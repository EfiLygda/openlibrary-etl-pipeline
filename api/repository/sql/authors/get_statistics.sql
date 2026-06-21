SELECT
    a.author_key,

    astats.top_work,
    astats.work_count,

    astats.ratings_count_1,
    astats.ratings_count_2,
    astats.ratings_count_3,
    astats.ratings_count_4,
    astats.ratings_count_5,

    astats.readinglog_count,
    astats.want_to_read_count,
    astats.currently_reading_count,
    astats.already_read_count
FROM
    authors AS a
    LEFT JOIN authors_statistics AS astats
    ON a.author_key = astats.author_key
WHERE
    a.author_key = %(filter_key)s
