CREATE TABLE IF NOT EXISTS works_time_periods
    (
        work_key VARCHAR NOT NULL,
        time_period VARCHAR NOT NULL,

        PRIMARY KEY (work_key, time_period),

        CONSTRAINT fk_works_time_periods_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );