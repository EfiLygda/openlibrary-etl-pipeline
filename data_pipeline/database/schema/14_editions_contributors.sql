CREATE TABLE IF NOT EXISTS catalog.editions_contributors
    (
        contribution_id SERIAL PRIMARY KEY,
        edition_key TEXT,
        contributor_name TEXT,
        contributor_role TEXT,
        by_statement TEXT,
        translated_from TEXT,
        translation_of TEXT,

        CONSTRAINT fk_editions_contributors_edition_key
            FOREIGN KEY (edition_key)
            REFERENCES catalog.editions(edition_key)
    );