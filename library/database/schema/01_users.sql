CREATE TABLE IF NOT EXISTS library.users (
    user_id         TEXT PRIMARY KEY,
    first_name      TEXT,
    last_name       TEXT,
    email           TEXT UNIQUE,
    registered_at   TIMESTAMP
);