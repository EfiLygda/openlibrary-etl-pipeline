
WITH

-- Calculates total editions for current author key
-- Returns only one row since authors_works does not have duplicates

total_editions_for_author AS (
    SELECT
        aw.author_key,
        COUNT(e.edition_key) AS record_count
    FROM
        authors_works AS aw
        INNER JOIN editions AS e
        ON aw.work_key = e.work_key
    WHERE
        author_key = %(filter_key)s
    GROUP BY
        author_key
),

-- Filters current author key's edition data with options
-- to limit and offset
-- Records are ordered by ascending edition key in order
-- for limit and offset to be deterministic
-- Returns one or more rows depending if the author has
-- one or editions

filtered_edition_records AS (
    SELECT
        aw.author_key,
        e.edition_key,
        e.title,
        e.subtitle,
        e.edition_name
    FROM
        authors_works AS aw
        INNER JOIN editions AS e
        ON aw.work_key = e.work_key
    WHERE
        aw.author_key = %(filter_key)s
    ORDER BY
        e.edition_key ASC
    LIMIT
        %(limit)s
    OFFSET
        %(offset)s
),

-- Aggregates all edition data for current author key
-- in a json object
-- Returns only one row since filtered_edition_records
-- has only one author key

json_aggregated_editions AS (
    SELECT
        author_key,
        COALESCE(
            json_agg(
                json_build_object(
                    'edition_key', edition_key,
                    'title', title,
                    'subtitle', subtitle,
                    'name', edition_name
                )
            ) FILTER (WHERE author_key IS NOT NULL),
            '[]'::json
        ) AS records
    FROM
        filtered_edition_records
    GROUP BY
        author_key
)

-- Join the json aggregated edition data with the
-- total number of editions via the author key
-- Returns only one row since both tables have
-- only one author key

SELECT
   jaa.author_key,
   ta.record_count,
   jaa.records
FROM
    json_aggregated_editions AS jaa
    INNER JOIN total_editions_for_author AS ta
    ON jaa.author_key = ta.author_key;
