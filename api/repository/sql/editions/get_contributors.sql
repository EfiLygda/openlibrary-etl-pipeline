SELECT
    contributor_name,
    contributor_role,
    by_statement,
    translated_from,
    translation_of
FROM
    editions_contributors
WHERE
    edition_key = %(filter_key)s
