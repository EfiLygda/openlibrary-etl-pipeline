SELECT
    w.work_key,
    ws.subjects,
    wpl.people,
    wpc.places,
    wtp.time_periods
FROM
    catalog.works w
    LEFT JOIN
    (
        SELECT work_key, array_agg(subject) AS subjects
        FROM catalog.works_subjects
        GROUP BY work_key
    ) ws ON w.work_key = ws.work_key
    LEFT JOIN
    (
        SELECT work_key, array_agg(person) AS people
        FROM catalog.works_people
        GROUP BY work_key
    ) wpl ON w.work_key = wpl.work_key
    LEFT JOIN (
        SELECT work_key, array_agg(place) AS places
        FROM catalog.works_places
        GROUP BY work_key
    ) wpc ON w.work_key = wpc.work_key
    LEFT JOIN (
        SELECT work_key, array_agg(time_period) AS time_periods
        FROM catalog.works_time_periods
        GROUP BY work_key
    ) wtp ON w.work_key = wtp.work_key
WHERE
    w.work_key = %(filter_key)s;
