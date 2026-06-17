SELECT
    description,
    notes,
    first_sentence
FROM
    editions_contents
WHERE
    edition_key = %(filter_key)s
