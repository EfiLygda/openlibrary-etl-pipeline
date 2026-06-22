SELECT
    COUNT(DISTINCT work_key)
FROM
    works
WHERE
    work_key = ANY(%(filter_key)s)