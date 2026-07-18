CREATE TABLE IF NOT EXISTS works_places
    (
        work_key VARCHAR NOT NULL,
        place VARCHAR NOT NULL,

        PRIMARY KEY (work_key, place),

        CONSTRAINT fk_works_places_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );