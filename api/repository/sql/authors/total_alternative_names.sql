SELECT
    COUNT(DISTINCT a.author_key) AS total_authors,
    COUNT(DISTINCT aan.author_alternative_name) AS total_names
FROM
    authors AS a
    LEFT JOIN authors_alternative_names AS aan
    ON a.author_key = aan.author_key
WHERE
    a.author_key = %(filter_key)s