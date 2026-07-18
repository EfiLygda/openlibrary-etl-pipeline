CREATE TABLE IF NOT EXISTS catalog.works
    (
        work_key TEXT PRIMARY KEY,
        title TEXT,
        subtitle TEXT,
        description TEXT,
        first_sentence TEXT,
        edition_count INT,
        first_publish_year INT,
        first_publish_date TEXT
    );