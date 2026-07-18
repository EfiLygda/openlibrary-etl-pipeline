SELECT
    COUNT(DISTINCT edition_key)
FROM
    catalog.editions
WHERE
    edition_key = ANY(%(filter_key)s)