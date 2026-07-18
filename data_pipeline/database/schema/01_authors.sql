CREATE TABLE IF NOT EXISTS catalog.authors
    (
        author_key TEXT PRIMARY KEY,
        author_name TEXT,
        bio TEXT,
        birth_date TEXT,
        death_date TEXT,
        birth_year INT,
        death_year INT
    );