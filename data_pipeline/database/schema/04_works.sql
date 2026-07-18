CREATE TABLE IF NOT EXISTS works
    (
        work_key VARCHAR PRIMARY KEY,
        title VARCHAR,
        subtitle VARCHAR,
        description TEXT,
        first_sentence TEXT,
        edition_count INT,
        first_publish_year INT,
        first_publish_date VARCHAR
    );