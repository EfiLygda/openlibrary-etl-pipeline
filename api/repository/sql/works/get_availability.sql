SELECT
    ebook_access,
    has_fulltext,
    has_public_scan
FROM
    works_availability
WHERE
    work_key = %(filter_key)s
