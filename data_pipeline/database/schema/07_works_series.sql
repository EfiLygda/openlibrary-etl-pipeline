CREATE TABLE IF NOT EXISTS works_series
    (
        work_key VARCHAR PRIMARY KEY,
        series_key VARCHAR,
        series_position VARCHAR,
        series_name VARCHAR,

        CONSTRAINT fk_works_series_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );