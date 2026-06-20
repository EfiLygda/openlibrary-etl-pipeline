SELECT
    COALESCE(
        array_agg(author_alternative_name)
            FILTER (WHERE author_alternative_name IS NOT NULL),
        ARRAY[]::text[]
    ) AS author_alternative_names
FROM
    authors_alternative_names AS altnames
WHERE
    author_key = %(filter_key)s
GROUP BY
    author_key