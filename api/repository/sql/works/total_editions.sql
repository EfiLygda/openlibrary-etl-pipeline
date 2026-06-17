SELECT
    COUNT(*) AS total
FROM
    editions
WHERE
    work_key = %(filter_key)s