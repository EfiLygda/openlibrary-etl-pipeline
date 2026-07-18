SELECT
    COUNT(DISTINCT aw.author_key) AS total_authors,
    COUNT(w.work_key) AS total_works
FROM
    catalog.authors_works AS aw
    LEFT JOIN catalog.works AS w
    ON aw.work_key = w.work_key
WHERE
    aw.author_key = %(filter_key)s