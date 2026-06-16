
WITH

-- Calculates total authors for current work key
-- Returns only one row since authors_works does not have duplicates

total_authors_for_work AS (
    SELECT
        work_key,
        COUNT(author_key) AS record_count
    FROM
        authors_works
    WHERE
        work_key = %(filter_key)s
    GROUP BY
        work_key
),

-- Filters current work key's author data with options
-- to limit and offset
-- Records are ordered by ascending author key in order
-- for limit and offset to be deterministic
-- Returns one or more rows depending if the work has
-- one or authors

filtered_author_records AS (
    SELECT
        aw.work_key,
        a.author_key,
        a.author_name,
        a.birth_year,
        a.death_year
    FROM
        authors AS a
        INNER JOIN authors_works AS aw
        ON a.author_key = aw.author_key
    WHERE
        aw.work_key = %(filter_key)s
    ORDER BY
        a.author_key ASC
    LIMIT
        %(limit)s
    OFFSET
        %(offset)s
),

-- Aggregates all author data for current work key
-- in a json object
-- Returns only one row since filtered_author_records
-- has only one work key

json_aggregated_authors AS (
    SELECT
        work_key,
        COALESCE(
            json_agg(
                json_build_object(
                    'author_key', author_key,
                    'author_name', author_name,
                    'birth_year', birth_year,
                    'death_year', death_year
                )
            ) FILTER (WHERE author_key IS NOT NULL),
            '[]'::json
        ) AS records
    FROM
        filtered_author_records
    GROUP BY
        work_key
)

-- Join the json aggregated author data with the
-- total number of authors via the work key
-- Returns only one row since both tables have
-- only one work key

SELECT
   jaa.work_key,
   ta.record_count,
   jaa.records
FROM
    json_aggregated_authors AS jaa
    INNER JOIN total_authors_for_work AS ta
    ON jaa.work_key = ta.work_key;