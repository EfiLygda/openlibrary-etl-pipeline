CREATE TABLE IF NOT EXISTS catalog.works_people
    (
        work_key TEXT NOT NULL,
        person TEXT NOT NULL,

        PRIMARY KEY (work_key, person),

        CONSTRAINT fk_works_people_work_key
            FOREIGN KEY (work_key)
            REFERENCES catalog.works(work_key)
    );