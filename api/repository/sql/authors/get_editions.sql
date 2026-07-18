SELECT
    e.edition_key,
    e.title,
    e.subtitle,
    e.edition_name
FROM
    catalog.authors AS a
    LEFT JOIN catalog.authors_works AS aw
    ON a.author_key = aw.author_key
    LEFT JOIN catalog.editions AS e
    ON aw.work_key = e.work_key
WHERE
    a.author_key = %(filter_key)s
ORDER BY
    e.title
LIMIT
    %(limit)s
OFFSET
    %(offset)s