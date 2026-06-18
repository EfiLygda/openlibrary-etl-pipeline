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
)

SELECT  COUNT(DISTINCT work_key)
FROM    works_results;