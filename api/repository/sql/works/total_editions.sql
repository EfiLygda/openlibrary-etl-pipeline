SELECT
    COUNT(DISTINCT w.work_key) AS total_works,
    COUNT(edition_key) AS total_editions
FROM
    catalog.works AS w
    LEFT JOIN catalog.editions AS e
    ON w.work_key = e.work_key
WHERE
    w.work_key = %(filter_key)s