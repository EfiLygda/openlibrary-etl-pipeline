SELECT
    COUNT(DISTINCT edition_key)
FROM
    editions
WHERE
    edition_key = ANY(%(filter_key)s)