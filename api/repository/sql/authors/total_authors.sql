SELECT
    COUNT(DISTINCT author_key)
FROM
    catalog.authors
WHERE
    author_key = ANY(%(filter_key)s)