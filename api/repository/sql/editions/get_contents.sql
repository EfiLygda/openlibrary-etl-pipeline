SELECT
    description,
    notes,
    first_sentence
FROM
    catalog.editions_contents
WHERE
    edition_key = %(filter_key)s
