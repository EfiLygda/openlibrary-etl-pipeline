
WITH

-- Calculates total editions for current work key
-- Returns only one row since editions does not have duplicates

total_editions_for_work AS (
    SELECT
        work_key,
        COUNT(edition_key) AS record_count
    FROM
        editions
    WHERE
        work_key = %(filter_key)s
    GROUP BY
        work_key
),

-- Filters current work key's edition data with options
-- to limit and offset
-- Records are ordered by ascending edition key in order
-- for limit and offset to be deterministic
-- Returns one or more rows depending if the work has
-- one or more editions

filtered_edition_records AS (
    SELECT
        work_key,
        edition_key,
        title,
        subtitle,
        edition_name
    FROM
        editions
    WHERE
        work_key = %(filter_key)s
    ORDER BY
        edition_key ASC
    LIMIT
        %(limit)s
    OFFSET
        %(offset)s
),

-- Aggregates all edition data for current work key
-- in a json object
-- Returns only one row since filtered_edition_records
-- has only one work key

json_aggregated_editions AS (
    SELECT
        work_key,
        COALESCE(
            json_agg(
                json_build_object(
                    'edition_key', edition_key,
                    'title', title,
                    'subtitle', subtitle,
                    'name', edition_name
                )
            ) FILTER (WHERE edition_key IS NOT NULL),
            '[]'::json
        ) AS records
    FROM
        filtered_edition_records
    GROUP BY
        work_key
)

-- Join the json aggregated edition data with the
-- total number of editions via the work key
-- Returns only one row since both tables have
-- only one work key

SELECT
   jaa.work_key,
   ta.record_count,
   jaa.records
FROM
    json_aggregated_editions AS jaa
    INNER JOIN total_editions_for_work AS ta
    ON jaa.work_key = ta.work_key;
