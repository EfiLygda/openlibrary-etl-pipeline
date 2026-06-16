
SELECT
    e.edition_key,
    COUNT(ec.edition_key) AS record_count,
    COALESCE(
        json_agg(
            json_build_object(
                'contributor_name', ec.contributor_name,
                'contributor_role', ec.contributor_role,
                'by_statement', ec.by_statement,
                'translated_from', ec.translated_from,
                'translation_of', ec.translation_of
            )
        ) FILTER (WHERE ec.edition_key IS NOT NULL),
        '[]'::json
    ) AS records
FROM
    editions AS e
    LEFT JOIN editions_contributors AS ec
    ON e.edition_key = ec.edition_key
WHERE
    e.edition_key = %(filter_key)s
GROUP BY
    e.edition_key;