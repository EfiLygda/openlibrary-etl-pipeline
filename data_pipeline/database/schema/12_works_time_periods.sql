CREATE TABLE IF NOT EXISTS catalog.works_time_periods
    (
        work_key TEXT NOT NULL,
        time_period TEXT NOT NULL,

        PRIMARY KEY (work_key, time_period),

        CONSTRAINT fk_works_time_periods_work_key
            FOREIGN KEY (work_key)
            REFERENCES catalog.works(work_key)
    );