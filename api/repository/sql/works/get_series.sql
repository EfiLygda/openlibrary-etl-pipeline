SELECT
    series_key,
    series_position,
    series_name
FROM
    catalog.works_series
WHERE
    work_key = %(filter_key)s
LIMIT
    %(limit)s
OFFSET
    %(offset)s
