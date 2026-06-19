SELECT
    COUNT(DISTINCT e.edition_key) AS total_editions,
    COUNT(w.work_key) AS total_works
FROM
    editions AS e
    INNER JOIN works AS w
    ON e.work_key = w.work_key
WHERE
    edition_key = %(filter_key)s