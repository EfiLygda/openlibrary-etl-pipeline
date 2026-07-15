CREATE TABLE IF NOT EXISTS copies (
    copy_id         TEXT PRIMARY KEY,
    edition_key     TEXT,
    status          TEXT,
    registered_at   TIMESTAMP,

    CONSTRAINT fk_copies_edition_key
        FOREIGN KEY (edition_key)
        REFERENCES editions(edition_key)
);