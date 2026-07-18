SELECT
    publish_date,
    publish_year,
    publisher,
    publish_place,
    publish_country,
    series AS series_title
FROM
    catalog.editions_publishing
WHERE
    edition_key = %(filter_key)s
