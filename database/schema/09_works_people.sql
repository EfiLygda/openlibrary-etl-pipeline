CREATE TABLE IF NOT EXISTS works_people
    (
        work_key VARCHAR NOT NULL,
        person VARCHAR NOT NULL,

        PRIMARY KEY (work_key, person),

        CONSTRAINT fk_works_people_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );