
SELECT
    e.edition_key,
    COUNT(ed.edition_key) AS record_count,
    COALESCE(
        json_agg(
            json_build_object(
                'number_of_pages', ed.number_of_pages,
                'physical_format', ed.physical_format,
                'physical_dimensions', ed.physical_dimensions,
                'weight', ed.weight,
                'language', ed.language
            )
        ) FILTER (WHERE ed.edition_key IS NOT NULL),
        '[]'::json
    ) AS records
FROM
    editions AS e
    LEFT JOIN editions_details AS ed
    ON e.edition_key = ed.edition_key
WHERE
    e.edition_key = %(filter_key)s
GROUP BY
    e.edition_key;