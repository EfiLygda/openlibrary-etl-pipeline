
WITH

-- Calculates total works for current author key
-- Returns only one row since authors_works does not have duplicates

total_works_for_author AS (
    SELECT
        author_key,
        COUNT(work_key) AS record_count
    FROM
        authors_works
    WHERE
        author_key = %(filter_key)s
    GROUP BY
        author_key
),

-- Filters current author key's author data with options
-- to limit and offset
-- Records are ordered by ascending work key in order
-- for limit and offset to be deterministic
-- Returns one or more rows depending if the work has
-- one or works

filtered_work_records AS (
    SELECT
        aw.author_key,
        w.work_key,
        w.title,
        w.subtitle,
        w.edition_count,
        w.first_publish_year
    FROM
        works AS w
        INNER JOIN authors_works AS aw
        ON w.work_key = aw.work_key
    WHERE
        aw.author_key = %(filter_key)s
    ORDER BY
        w.work_key ASC
    LIMIT
        %(limit)s
    OFFSET
        %(offset)s
),

-- Aggregates all work data for current author key
-- in a json object
-- Returns only one row since filtered_work_records
-- has only one author key

json_aggregated_works AS (
    SELECT
        author_key,
        COALESCE(
            json_agg(
                json_build_object(
                    'work_key', work_key,
                    'title', title,
                    'subtitle', subtitle,
                    'edition_count', edition_count,
                    'first_publish_year', first_publish_year
                )
            ) FILTER (WHERE work_key IS NOT NULL),
            '[]'::json
        ) AS records
    FROM
        filtered_work_records
    GROUP BY
        author_key
)

-- Join the json aggregated work data with the
-- total number of works via the author key
-- Returns only one row since both tables have
-- only one author key

SELECT
   jaa.author_key,
   ta.record_count,
   jaa.records
FROM
    json_aggregated_works AS jaa
    INNER JOIN total_works_for_author AS ta
    ON jaa.author_key = ta.author_key;
