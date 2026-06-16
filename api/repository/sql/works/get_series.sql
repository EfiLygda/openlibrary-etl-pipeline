
WITH

-- Calculates total series for current work key
-- Returns only one row since series does not have duplicates

total_series_for_work AS (
    SELECT
        work_key,
        COUNT(series_key) AS record_count
    FROM
        works_series
    WHERE
        work_key = %(filter_key)s
    GROUP BY
        work_key
),

-- Filters current work key's series data with options
-- to limit and offset
-- Records are ordered by ascending series key in order
-- for limit and offset to be deterministic
-- Returns one or more rows depending if the work has
-- one or series

filtered_series_records AS (
    SELECT
        work_key,
        series_key,
        series_position,
        series_name
    FROM
        works_series
    WHERE
        work_key = %(filter_key)s
    ORDER BY
        series_key ASC
    LIMIT
        %(limit)s
    OFFSET
        %(offset)s
),

-- Aggregates all series data for current work key
-- in a json object
-- Returns only one row since filtered_series_records
-- has only one work key

json_aggregated_series AS (
    SELECT
        work_key,
        COALESCE(
            json_agg(
                json_build_object(
                    'series_key', series_key,
                    'series_position', series_position,
                    'series_name', series_name
                )
            ) FILTER (WHERE series_key IS NOT NULL),
            '[]'::json
        ) AS records
    FROM
        filtered_series_records
    GROUP BY
        work_key
)

-- Join the json aggregated series data with the
-- total number of series via the work key
-- Returns only one row since both tables have
-- only one work key

SELECT
   jaa.work_key,
   ta.record_count,
   jaa.records
FROM
    json_aggregated_series AS jaa
    INNER JOIN total_series_for_work AS ta
    ON jaa.work_key = ta.work_key;
