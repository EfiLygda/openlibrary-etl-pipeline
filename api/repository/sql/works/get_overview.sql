
SELECT
    w.work_key,

    CASE
        WHEN ws.subjects IS NULL
         AND wpl.people IS NULL
         AND wpc.places IS NULL
         AND wtp.time_periods IS NULL
        THEN 0
        ELSE 1
    END AS record_count,

    CASE
        WHEN ws.subjects IS NULL
         AND wpl.people IS NULL
         AND wpc.places IS NULL
         AND wtp.time_periods IS NULL
        THEN '[]'::json
        ELSE json_agg(
            json_build_object(
                'subjects', ws.subjects,
                'people', wpl.people,
                'places', wpc.places,
                'time_periods', wtp.time_periods
            )
        )
    END AS records
FROM
    works w
    LEFT JOIN
    (
        SELECT work_key, array_agg(subject) AS subjects
        FROM works_subjects
        GROUP BY work_key
    ) ws ON w.work_key = ws.work_key
    LEFT JOIN
    (
        SELECT work_key, array_agg(person) AS people
        FROM works_people
        GROUP BY work_key
    ) wpl ON w.work_key = wpl.work_key
    LEFT JOIN (
        SELECT work_key, array_agg(place) AS places
        FROM works_places
        GROUP BY work_key
    ) wpc ON w.work_key = wpc.work_key
    LEFT JOIN (
        SELECT work_key, array_agg(time_period) AS time_periods
        FROM works_time_periods
        GROUP BY work_key
    ) wtp ON w.work_key = wtp.work_key
WHERE
    w.work_key = %(filter_key)s
GROUP BY
    w.work_key,
    ws.subjects,
    wpl.people,
    wpc.places,
    wtp.time_periods;