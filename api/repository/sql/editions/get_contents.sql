
SELECT
    e.edition_key,
    COUNT(ec.edition_key) AS record_count,
    COALESCE(
        json_agg(
            json_build_object(
                'description', ec.description,
                'notes', ec.notes,
                'first_sentence', ec.first_sentence
            )
        ) FILTER (WHERE ec.edition_key IS NOT NULL),
        '[]'::json
    ) AS records
FROM
    editions AS e
    LEFT JOIN
    editions_contents AS ec
    ON e.edition_key = ec.edition_key
WHERE
    e.edition_key = %(filter_key)s
GROUP BY
    e.edition_key;