
WITH

-- Calculates total availability for current work key
-- Returns only one row since availability does not have duplicates

total_availability_for_work AS (
    SELECT
        work_key,
        COUNT(work_key) AS record_count
    FROM
        works_availability
    WHERE
        work_key = %(filter_key)s
    GROUP BY
        work_key
),

-- Filters current work key's availability data with options
-- to limit and offset
-- Records are ordered by ascending availability key in order
-- for limit and offset to be deterministic
-- Returns one or more rows depending if the work has
-- one or availability

filtered_availability_records AS (
    SELECT
        work_key,
        ebook_access,
        has_fulltext,
        has_public_scan
    FROM
        works_availability
    WHERE
        work_key = %(filter_key)s
    ORDER BY
        work_key ASC
    LIMIT
        %(limit)s
    OFFSET
        %(offset)s
),

-- Aggregates all availability data for current work key
-- in a json object
-- Returns only one row since filtered_availability_records
-- has only one work key

json_aggregated_availability AS (
    SELECT
        work_key,
        COALESCE(
            json_agg(
                json_build_object(
                    'ebook_access', ebook_access,
                    'has_fulltext', has_fulltext,
                    'has_public_scan', has_public_scan
                )
            ) FILTER (WHERE work_key IS NOT NULL),
            '[]'::json
        ) AS records
    FROM
        filtered_availability_records
    GROUP BY
        work_key
)

-- Join the json aggregated availability data with the
-- total number of availability via the work key
-- Returns only one row since both tables have
-- only one work key

SELECT
   jaa.work_key,
   ta.record_count,
   jaa.records
FROM
    json_aggregated_availability AS jaa
    INNER JOIN total_availability_for_work AS ta
    ON jaa.work_key = ta.work_key;
