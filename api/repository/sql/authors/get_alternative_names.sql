WITH filtered_alternative_names AS (
    SELECT
        a.author_name,
        altnames.author_alternative_name
    FROM
        authors a
        LEFT JOIN authors_alternative_names altnames
        ON a.author_key = altnames.author_key
    WHERE
        a.author_key = %(filter_key)s
    LIMIT
        %(limit)s
    OFFSET
        %(offset)s
)

SELECT
    author_name,
    COALESCE(
        array_agg(author_alternative_name)
            FILTER (WHERE author_alternative_name IS NOT NULL),
        ARRAY[]::text[]
    ) AS alternative_names
FROM
    filtered_alternative_names
GROUP BY
    author_name