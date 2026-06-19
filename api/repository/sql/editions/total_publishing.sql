SELECT
    COUNT(DISTINCT e.edition_key) AS total_editions,
    COUNT(ed.edition_key) AS total_publishing
FROM
    editions AS e
    LEFT JOIN editions_publishing AS ed
    ON e.edition_key = ed.edition_key
WHERE
    e.edition_key = %(filter_key)s