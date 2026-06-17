SELECT
    COUNT(*) AS total
FROM
    authors_works
WHERE
    work_key = %(filter_key)s