SELECT
    w.work_key,
    w.title,
    w.subtitle,
    w.edition_count,
    w.first_publish_year
FROM
    editions AS e
    INNER JOIN works AS w
    ON e.work_key = w.work_key
WHERE
    edition_key = %(filter_key)s