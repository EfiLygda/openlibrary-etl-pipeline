SELECT
    work_key,
    ebook_access,
    has_fulltext,
    has_public_scan
FROM
    catalog.works_availability
WHERE
    work_key = %(filter_key)s
