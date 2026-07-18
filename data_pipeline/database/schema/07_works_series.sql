CREATE TABLE IF NOT EXISTS catalog.works_series
    (
        work_key TEXT PRIMARY KEY,
        series_key TEXT,
        series_position TEXT,
        series_name TEXT,

        CONSTRAINT fk_works_series_work_key
            FOREIGN KEY (work_key)
            REFERENCES catalog.works(work_key)
    );