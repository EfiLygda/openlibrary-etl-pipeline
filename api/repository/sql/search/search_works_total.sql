------------------------------------------------------------------------------------------
-- This query aims to find and sort works by trigram similarity of the give query
-- The given query will be compared with these fields in the database

-- 1. work title and subtitle
-- 2. author name
-- 3. work subjects
-- 4. work people
-- 5. work places
-- 6. work time periods
-- 7. editions title and subtitle
-- 8. work series name
------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------
-- The final text relevance score is calculated as:

-- 1. Trigram similarity is calculated for the fields
--    works.title, works.subtitle,
--    authors.author_name,
--    authors_alternative_names.author_alternative_name,
--    works_subjects.subject,
--    works_people.person,
--    works_places.place,
--    works_time_periods.time_period,
--    editions.title, editions.subtitle.
--    works_series.series_name

-- 2. When a field has a similarity score less than 0.3 then it is filtered out

-- 3. In case there are two fields in a table for the similarity to be used on
-- (like works and editions title and subtitle), then the maximum similarity is used

-- 4. Each table, except works is grouped by work key and the maximum similarity scored is used

-- 5. Each similarity, after the grouping, is multiplied by a weight:
--  0.3 * works
--  0.2 * authors
--  0.1 * authors_alternative_names
--  0.1 * subjects
--  0.1 * people
--  0.05 * places
--  0.05 * time_periods
--  0.05 * editions
--  0.05 * work_series

-- 6. For each work the final score is calculated by summing up all scores
--    Final scores are in [0.3,1]
------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------
-- Preparing for the query --

-- Install pg_trgm in order to use trigram operator for filtering
-- and 'similarity' function for calculating the trigram similarity
-- between the given query and a string
--CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Setting the similarity score limit for filtering out works from the results
-- Works where a similarity score is lower than 0.3 will be filtered out
SELECT set_limit(0.3);
------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------
-- CTEs used for calculations ---
WITH 

-- Calculating the weighted scores for the results, while also filtering results out
weighted_work_results AS (

	SELECT  
	    work_key, 
	    0.3 * GREATEST(                             -- Maximum value per row
	        similarity(title, %(query)s),
	        similarity(subtitle, %(query)s)
        ) AS score
	FROM    
	    catalog.works
	WHERE   
	    title %% %(query)s OR subtitle %% %(query)s -- Filtering out by less than 0.3 similarity score

	UNION ALL

	SELECT  
	    aw.work_key,
	    0.2 * MAX(
	        similarity(a.author_name, %(query)s)
	    ) AS score
	FROM    
	    catalog.authors_works AS aw
        INNER JOIN catalog.authors AS a
        ON aw.author_key = a.author_key
	WHERE   
	    a.author_name %% %(query)s
	GROUP BY
	    aw.work_key

	UNION ALL

	SELECT  
	    aw.work_key,
	    0.1 * MAX(
	        similarity(an.author_alternative_name, %(query)s)
        ) AS score
	FROM    
	    catalog.authors_works AS aw
        INNER JOIN catalog.authors_alternative_names AS an
        ON aw.author_key = an.author_key
	WHERE   
	    an.author_alternative_name %% %(query)s
	GROUP BY
	    aw.work_key

	UNION ALL

	SELECT  
	    work_key,
	    0.1 * MAX(
	        similarity(subject, %(query)s)
	    ) AS score
	FROM    
	    catalog.works_subjects
	WHERE   
	    subject %% %(query)s
    GROUP BY
	    work_key

	UNION ALL

	SELECT
	    work_key,
	    0.1 * MAX(
	        similarity(person, %(query)s)
	    ) AS score
	FROM
	    catalog.works_people
	WHERE
	    person %% %(query)s
    GROUP BY
	    work_key

	UNION ALL

	SELECT
	    work_key,
	    0.05 * MAX(
	        similarity(place, %(query)s)
	    ) AS score
	FROM
	    catalog.works_places
	WHERE
	    place %% %(query)s
    GROUP BY
	    work_key

	UNION ALL

	SELECT
	    work_key,
	    0.05 * MAX(
	        similarity(time_period, %(query)s)
        ) AS score
	FROM
	    catalog.works_time_periods
	WHERE
	    time_period %% %(query)s
    GROUP BY
	    work_key

	UNION ALL

	SELECT
	    work_key,
	    0.05 * MAX(
	        GREATEST(
                similarity(title, %(query)s),
                similarity(subtitle, %(query)s)
	        )
	    ) AS score
	FROM
	    catalog.editions
	WHERE
	    title %% %(query)s OR subtitle %% %(query)s
    GROUP BY
	    work_key

	UNION ALL

	SELECT
	    work_key,
	    0.05 * MAX(
	        similarity(series_name, %(query)s)
	    ) AS score
	FROM
	    catalog.works_series
	WHERE
	    series_name %% %(query)s
    GROUP BY
	    work_key
),

-- Calculating final relevance scores via summing up the weighted scores
text_relevance_scores AS (
	SELECT
	    work_key,
	    SUM(score) AS score
	FROM
	    weighted_work_results
	GROUP BY
	    work_key
)
------------------------------------------------------------------------------------------

------------------------------------------------------------------------------------------
-- Calculating final results count
SELECT
    COUNT(DISTINCT w.work_key)
FROM
    catalog.works AS w
    INNER JOIN text_relevance_scores AS trs
    ON w.work_key = trs.work_key
WHERE

    -- Optional exact year filter
    (
        %(year)s IS NULL                            -- In case no year is passed this returns TRUE
        OR (                                        -- If a year is given:
            w.first_publish_year = %(year)s         -- 2. First publish year is the given year
            AND w.first_publish_year IS NOT NULL    -- 1. First publish year is not null
        )
    )

    AND

    -- Optional EDITION language filter
    -- NOTE: no primary language exists in the dataset for works
    --       so this searches via the editions languages
    (
        %(lang)s IS NULL                                -- In case no language is passed this returns TRUE
        OR (                                                -- If a language is given:
            EXISTS (                                        -- Returns True if the current work is found to have
                                                            -- at least one edition with the given language
                SELECT                                      -- 1. Select only row
                    1
                FROM
                    catalog.editions AS e                           -- 2. Add to editions, editions_details since it
                    INNER JOIN catalog.editions_details AS ed       --    includes the language field
                    ON e.edition_key = ed.edition_key
                WHERE
                    e.work_key = w.work_key                 -- 3. Filter for current work
                    AND ed.language = %(lang)s          -- 4. Filter for current given language
            )
        )
    )
    
    AND

    (
        %(published_by)s IS NULL
        OR (
            EXISTS (
                SELECT
                    1
                FROM
                    catalog.editions AS e
                    INNER JOIN catalog.editions_publishing AS ep
                    ON e.edition_key = ep.edition_key
                WHERE
                    e.work_key = w.work_key
                    AND ep.publisher %% %(published_by)s
            )
        )
    )
;
