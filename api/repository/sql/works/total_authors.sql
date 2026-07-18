SELECT
    COUNT(DISTINCT w.work_key) AS total_works,
    COUNT(author_key) AS total_authors
FROM
    catalog.works AS w
    LEFT JOIN catalog.authors_works AS aw
    ON w.work_key = aw.work_key
WHERE
    w.work_key = %(filter_key)s