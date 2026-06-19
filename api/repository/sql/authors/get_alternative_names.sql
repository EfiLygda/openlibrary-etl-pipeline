
-- Counts total alternative names for an author key
-- and aggregates the names in an array

SELECT
    COALESCE(
        array_agg(altnames.author_alternative_name)
            FILTER (WHERE altnames.author_alternative_name IS NOT NULL),
        ARRAY[]::text[]
    ) AS author_alternative_names
FROM
    authors AS a
    LEFT JOIN
    authors_alternative_names AS altnames
    ON a.author_key = altnames.author_key
WHERE
    a.author_key = %(filter_key)s
GROUP BY
    a.author_key