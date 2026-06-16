
WITH

-- Calculates total author statistics for current author key
-- Returns only one row since author_statistics does not have duplicates

total_authors_statistics_for_author AS (
    SELECT
        a.author_key,
        COUNT(astat.author_key) AS record_count
    FROM
        authors AS a
        INNER JOIN authors_statistics AS astat
        ON a.author_key = astat.author_key
    WHERE
        a.author_key = %(filter_key)s
    GROUP BY
        a.author_key
),

-- Filters current author key's authors_statistics data with options
-- to limit and offset
-- Records are ordered by ascending author key in order
-- for limit and offset to be deterministic
-- Returns one or more rows depending if the author has
-- one or authors statistics

filtered_authors_statistics_records AS (
    SELECT
        a.author_key,

        astat.top_work,
        astat.work_count,

        astat.ratings_count_1,
        astat.ratings_count_2,
        astat.ratings_count_3,
        astat.ratings_count_4,
        astat.ratings_count_5,

        astat.readinglog_count,
        astat.want_to_read_count,
        astat.currently_reading_count,
        astat.already_read_count
    FROM
        authors AS a
        INNER JOIN authors_statistics AS astat
        ON a.author_key = astat.author_key
    WHERE
        a.author_key = %(filter_key)s
    ORDER BY
        astat.author_key ASC
    LIMIT
        %(limit)s
    OFFSET
        %(offset)s
),

-- Aggregates all authors statistics data for current author key
-- in a json object
-- Returns only one row since filtered_authors_statistics_records
-- has only one author key

json_aggregated_authors_statistics AS (
    SELECT
        author_key,
        COALESCE(
            json_agg(
                json_build_object(
                    'top_work', top_work,
                    'work_count', work_count,

                    'ratings_count_1', ratings_count_1,
                    'ratings_count_2', ratings_count_2,
                    'ratings_count_3', ratings_count_3,
                    'ratings_count_4', ratings_count_4,
                    'ratings_count_5', ratings_count_5,

                    'readinglog_count', readinglog_count,
                    'want_to_read_count', want_to_read_count,
                    'currently_reading_count', currently_reading_count,
                    'already_read_count', already_read_count
                )
            ) FILTER (WHERE author_key IS NOT NULL),
            '[]'::json
        ) AS records
    FROM
        filtered_authors_statistics_records
    GROUP BY
        author_key
)

-- Join the json aggregated authors statistics data with the
-- total number of authors statistics via the author key
-- Returns only one row since both tables have
-- only one author key

SELECT
   jaa.author_key,
   ta.record_count,
   jaa.records
FROM
    json_aggregated_authors_statistics AS jaa
    INNER JOIN total_authors_statistics_for_author AS ta
    ON jaa.author_key = ta.author_key;
