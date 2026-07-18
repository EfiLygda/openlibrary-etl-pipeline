CREATE TABLE IF NOT EXISTS catalog.works_subjects
    (
        work_key TEXT NOT NULL,
        subject TEXT NOT NULL,

        PRIMARY KEY (work_key, subject),

        CONSTRAINT fk_works_subjects_work_key
            FOREIGN KEY (work_key)
            REFERENCES catalog.works(work_key)
    );