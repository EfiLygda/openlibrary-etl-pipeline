CREATE TABLE IF NOT EXISTS editions_contributors
    (
        contribution_id SERIAL PRIMARY KEY,
        edition_key VARCHAR,
        contributor_name VARCHAR,
        contributor_role VARCHAR,
        by_statement VARCHAR,
        translated_from VARCHAR,
        translation_of VARCHAR,

        CONSTRAINT fk_editions_contributors_edition_key
            FOREIGN KEY (edition_key)
            REFERENCES editions(edition_key)
    );