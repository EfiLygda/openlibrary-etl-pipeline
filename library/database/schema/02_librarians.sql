CREATE TABLE IF NOT EXISTS librarians (
    librarian_id    SERIAL PRIMARY KEY,
    first_name      TEXT,
    last_name       TEXT,
    email           TEXT UNIQUE,
    registered_at   TIMESTAMP
);