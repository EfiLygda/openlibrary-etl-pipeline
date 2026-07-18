CREATE TABLE IF NOT EXISTS catalog.editions_details
    (
        details_id SERIAL PRIMARY KEY,
        edition_key TEXT,
        number_of_pages INT,
        physical_format TEXT,
        physical_dimensions TEXT,
        weight TEXT,
        language TEXT,

        CONSTRAINT fk_editions_details_edition_key
            FOREIGN KEY (edition_key)
            REFERENCES catalog.editions(edition_key)
    );