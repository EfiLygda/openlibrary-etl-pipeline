SELECT
    COUNT(DISTINCT a.author_key) AS total_authors,
    COUNT(astat.author_key) AS total_statistics
FROM
    authors AS a
    LEFT JOIN authors_statistics AS astat
    ON a.author_key = astat.author_key
WHERE
    a.author_key = %(filter_key)s