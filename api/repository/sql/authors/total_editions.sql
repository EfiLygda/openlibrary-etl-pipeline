SELECT
    COUNT(DISTINCT a.author_key) AS total_authors,
    COUNT(e.edition_key) AS total_editions
FROM
    authors AS a
    LEFT JOIN authors_works AS aw
    ON a.author_key = aw.author_key
    LEFT JOIN editions AS e
    ON aw.work_key = e.work_key
WHERE
    a.author_key = %(filter_key)s