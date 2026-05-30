CREATE TABLE IF NOT EXISTS editions_publishing
    (
        publishing_id SERIAL PRIMARY KEY,
        edition_key VARCHAR,
        publish_date VARCHAR,
        publish_year INT,
        publisher VARCHAR,
        publish_place VARCHAR,
        publish_country VARCHAR,
        series VARCHAR,

        CONSTRAINT fk_editions_publishing_edition_key
            FOREIGN KEY (edition_key)
            REFERENCES editions(edition_key)
    );