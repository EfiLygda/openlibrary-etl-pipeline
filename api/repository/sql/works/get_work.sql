SELECT
    *
FROM
    works
WHERE
    work_key = ANY(%(filter_key)s)
LIMIT
    %(limit)s
OFFSET
    %(offset)s