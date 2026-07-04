CREATE TABLE IF NOT EXISTS copies (
    copy_id         TEXT PRIMARY KEY,
    edition_key     TEXT,
    status          TEXT,
    registered_at   TIMESTAMP
);