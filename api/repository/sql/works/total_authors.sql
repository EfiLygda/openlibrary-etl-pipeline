SELECT
    COUNT(DISTINCT w.work_key) AS total_works,
    COUNT(author_key) AS total_authors
FROM
    works AS w
    LEFT JOIN authors_works AS aw
    ON w.work_key = aw.work_key
WHERE
    w.work_key = %(filter_key)s