SELECT
    a.author_key,
    a.author_name,
    a.birth_year,
    a.death_year
FROM
    catalog.works AS w
    INNER JOIN catalog.authors_works AS aw
    ON w.work_key = aw.work_key
    INNER JOIN catalog.authors AS a
    ON aw.author_key = a.author_key
WHERE
    w.work_key = %(filter_key)s
ORDER BY
    a.author_key
LIMIT
    %(limit)s
OFFSET
    %(offset)s