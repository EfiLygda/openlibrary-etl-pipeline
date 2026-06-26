SELECT
    work_key,
    ratings_count_1,
    ratings_count_2,
    ratings_count_3,
    ratings_count_4,
    ratings_count_5
FROM
    works_ratings
WHERE
    work_key = %(filter_key)s
