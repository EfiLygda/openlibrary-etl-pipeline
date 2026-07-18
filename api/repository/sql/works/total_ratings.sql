SELECT
    COUNT(DISTINCT w.work_key) AS total_works,
    COUNT(DISTINCT wr.work_key) AS total_ratings
FROM
    catalog.works AS w
    LEFT JOIN catalog.works_ratings AS wr
    ON w.work_key = wr.work_key
WHERE
    w.work_key = %(filter_key)s