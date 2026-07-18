CREATE TABLE IF NOT EXISTS authors
    (
        author_key VARCHAR PRIMARY KEY,
        author_name VARCHAR,
        bio VARCHAR,
        birth_date VARCHAR,
        death_date VARCHAR,
        birth_year INT,
        death_year INT
    );