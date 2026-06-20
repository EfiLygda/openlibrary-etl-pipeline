SELECT
    w.work_key,
    w.title,
    w.subtitle,
    w.edition_count,
    w.first_publish_year
FROM
    works AS w
    INNER JOIN authors_works AS aw
    ON w.work_key = aw.work_key
WHERE
    aw.author_key = %(filter_key)s
ORDER BY
    w.first_publish_year DESC
LIMIT
    %(limit)s
OFFSET
    %(offset)s
