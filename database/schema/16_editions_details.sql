CREATE TABLE IF NOT EXISTS editions_details
    (
        details_id SERIAL PRIMARY KEY,
        edition_key VARCHAR,
        number_of_pages INT,
        physical_format VARCHAR,
        physical_dimensions VARCHAR,
        weight VARCHAR,
        language VARCHAR,

        CONSTRAINT fk_editions_details_edition_key
            FOREIGN KEY (edition_key)
            REFERENCES editions(edition_key)
    );