SELECT
    COUNT(DISTINCT author_key)
FROM
    authors
WHERE
    author_key = ANY(%(filter_key)s)