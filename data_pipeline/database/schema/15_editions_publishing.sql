CREATE TABLE IF NOT EXISTS catalog.editions_publishing
    (
        publishing_id SERIAL PRIMARY KEY,
        edition_key TEXT,
        publish_date TEXT,
        publish_year INT,
        publisher TEXT,
        publish_place TEXT,
        publish_country TEXT,
        series TEXT,

        CONSTRAINT fk_editions_publishing_edition_key
            FOREIGN KEY (edition_key)
            REFERENCES catalog.editions(edition_key)
    );