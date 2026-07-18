SELECT
    COUNT(DISTINCT w.work_key) AS total_works,
    COUNT(DISTINCT wa.work_key) AS total_availability
FROM
    catalog.works AS w
    LEFT JOIN catalog.works_availability AS wa
    ON w.work_key = wa.work_key
WHERE
    w.work_key = %(filter_key)s