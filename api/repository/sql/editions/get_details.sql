SELECT
    number_of_pages,
    physical_format,
    physical_dimensions,
    weight,
    language
FROM
    catalog.editions_details
WHERE
    edition_key = %(filter_key)s
