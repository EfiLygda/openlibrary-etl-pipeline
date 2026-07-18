SELECT
    COUNT(DISTINCT work_key)
FROM
    catalog.works
WHERE
    work_key = ANY(%(filter_key)s)