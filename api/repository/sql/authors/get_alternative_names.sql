SELECT
    altnames.author_alternative_name
FROM
    authors AS a
    LEFT JOIN authors_alternative_names AS altnames
    ON a.author_key = altnames.author_key
WHERE
    a.author_key = %(filter_key)s
LIMIT
    %(limit)s
OFFSET
    %(offset)s