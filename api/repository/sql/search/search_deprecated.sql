WITH works_results AS (

	SELECT  work_key
	FROM    works
	WHERE   title ILIKE %(pattern)s OR subtitle ILIKE %(pattern)s

	UNION

	SELECT  aw.work_key
	FROM    authors_works AS aw
            INNER JOIN authors AS a
            ON aw.author_key = a.author_key
	WHERE   a.author_name ILIKE %(pattern)s

	UNION

	SELECT  aw.work_key
	FROM    authors_works AS aw
            INNER JOIN authors_alternative_names AS an
            ON aw.author_key = an.author_key
	WHERE   an.author_alternative_name ILIKE %(pattern)s

	UNION

	SELECT  work_key
	FROM    works_subjects
	WHERE   subject ILIKE %(pattern)s

	UNION

	SELECT  work_key
	FROM    works_people
	WHERE   person ILIKE %(pattern)s

	UNION

	SELECT  work_key
	FROM    works_places
	WHERE   place ILIKE %(pattern)s

	UNION

	SELECT  work_key
	FROM    works_time_periods
	WHERE   time_period ILIKE %(pattern)s

	UNION

	SELECT  work_key
	FROM    editions
	WHERE   title ILIKE %(pattern)s OR subtitle ILIKE %(pattern)s

	UNION

	SELECT  work_key
	FROM    works_series
	WHERE   series_name ILIKE %(pattern)s
),

added_search_scores AS (
    SELECT  res.work_key,
            w.title,
            a.author_key,
            a.author_name,
            CASE
                WHEN w.title ILIKE %(pattern)s THEN 3
                WHEN a.author_name ILIKE %(pattern)s THEN 2
                ELSE 1
            END as score

    FROM    works_results AS res
            INNER JOIN works AS w
            ON res.work_key = w.work_key

            INNER JOIN authors_works AS aw
            ON res.work_key = aw.work_key
            INNER JOIN authors AS a
            ON aw.author_key = a.author_key
),

convert_authors_to_json AS (

    SELECT      work_key,
                title,
                score,
                json_build_object(
                    'author_key', author_key,
                    'author_name', author_name
                )
                AS author
    FROM        added_search_scores
)

SELECT      work_key,
            title,
            json_agg(author) AS authors
FROM        convert_authors_to_json
GROUP BY    work_key, title
ORDER BY    SUM(score) DESC
LIMIT       %(limit)s
OFFSET      %(offset)s
;