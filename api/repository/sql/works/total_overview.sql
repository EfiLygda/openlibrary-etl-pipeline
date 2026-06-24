SELECT
    COUNT(DISTINCT work_key)
FROM
    works
WHERE
    work_key = %(filter_key)s