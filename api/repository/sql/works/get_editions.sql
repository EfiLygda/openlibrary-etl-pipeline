SELECT
    edition_key,
    title,
    subtitle,
    edition_name
FROM
    catalog.editions
WHERE
    work_key = %(filter_key)s
LIMIT
    %(limit)s
OFFSET
    %(offset)s