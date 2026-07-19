CREATE TYPE
    library.copy_status AS ENUM (
            'AVAILABLE',
            'UNAVAILABLE'
        );

CREATE TABLE IF NOT EXISTS library.copies (
    copy_id         TEXT PRIMARY KEY,
    edition_key     TEXT NOT NULL,
    status          library.copy_status,
    registered_at   TIMESTAMP,

    CONSTRAINT fk_copies_edition_key
        FOREIGN KEY (edition_key)
        REFERENCES catalog.editions(edition_key)
);