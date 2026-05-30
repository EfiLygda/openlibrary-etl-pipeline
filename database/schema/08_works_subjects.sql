CREATE TABLE IF NOT EXISTS works_subjects
    (
        work_key VARCHAR NOT NULL,
        subject VARCHAR NOT NULL,

        PRIMARY KEY (work_key, subject),

        CONSTRAINT fk_works_subjects_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );