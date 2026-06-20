SELECT
    e.edition_key,
    e.title,
    e.subtitle,
    e.edition_name
FROM
    authors_works AS aw
    LEFT JOIN editions AS e
    ON aw.work_key = e.work_key
WHERE
    aw.author_key = %(filter_key)s
ORDER BY
    e.title
LIMIT
    %(limit)s
OFFSET
    %(offset)s