
SELECT
    e.edition_key,
    COUNT(ep.edition_key) AS record_count,
    COALESCE(
        json_agg(
            json_build_object(
                'publish_date', ep.publish_date,
                'publish_year', ep.publish_year,
                'publisher', ep.publisher,
                'publish_place', ep.publish_place,
                'publish_country', ep.publish_country,
                'series_title', ep.series
            )
        ) FILTER (WHERE ep.edition_key IS NOT NULL),
        '[]'::json
    ) AS records
FROM
    editions AS e
    LEFT JOIN editions_publishing AS ep
    ON e.edition_key = ep.edition_key
WHERE
    e.edition_key = %(filter_key)s
GROUP BY
    e.edition_key
