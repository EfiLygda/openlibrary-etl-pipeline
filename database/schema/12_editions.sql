CREATE TABLE IF NOT EXISTS editions
    (
        edition_key VARCHAR PRIMARY KEY,
        work_key VARCHAR,
        title VARCHAR,
        subtitle VARCHAR,
        edition_name VARCHAR,

        CONSTRAINT fk_editions_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );