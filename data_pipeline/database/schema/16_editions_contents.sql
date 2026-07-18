CREATE TABLE IF NOT EXISTS catalog.editions_contents
    (
        edition_key TEXT PRIMARY KEY,
        description TEXT,
        notes TEXT,
        first_sentence TEXT,

        CONSTRAINT fk_editions_contents_edition_key
            FOREIGN KEY (edition_key)
            REFERENCES catalog.editions(edition_key)
    );