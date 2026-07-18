SELECT
    COUNT(DISTINCT work_key)
FROM
    catalog.works
WHERE
    work_key = %(filter_key)s