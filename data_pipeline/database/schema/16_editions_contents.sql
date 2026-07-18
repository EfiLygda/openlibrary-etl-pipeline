CREATE TABLE IF NOT EXISTS editions_contents
    (
        edition_key VARCHAR PRIMARY KEY,
        description VARCHAR,
        notes VARCHAR,
        first_sentence VARCHAR,

        CONSTRAINT fk_editions_contents_edition_key
            FOREIGN KEY (edition_key)
            REFERENCES editions(edition_key)
    );