SELECT
    COUNT(DISTINCT w.work_key) AS total_works,
    COUNT(series_key) AS total_series
FROM
    catalog.works AS w
    LEFT JOIN catalog.works_series AS s
    ON w.work_key = s.work_key
WHERE
    w.work_key = %(filter_key)s