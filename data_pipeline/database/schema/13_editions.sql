CREATE TABLE IF NOT EXISTS catalog.editions
    (
        edition_key TEXT PRIMARY KEY,
        work_key TEXT,
        title TEXT,
        subtitle TEXT,
        edition_name TEXT,

        CONSTRAINT fk_editions_work_key
            FOREIGN KEY (work_key)
            REFERENCES catalog.works(work_key)
    );