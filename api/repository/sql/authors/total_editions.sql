SELECT
    COUNT(DISTINCT aw.author_key) AS total_authors,
    COUNT(e.edition_key) AS total_editions
FROM
    authors_works AS aw
    LEFT JOIN editions AS e
    ON aw.work_key = e.work_key
WHERE
    aw.author_key = %(filter_key)s