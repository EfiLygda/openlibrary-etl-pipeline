CREATE TABLE IF NOT EXISTS catalog.works_places
    (
        work_key TEXT NOT NULL,
        place TEXT NOT NULL,

        PRIMARY KEY (work_key, place),

        CONSTRAINT fk_works_places_work_key
            FOREIGN KEY (work_key)
            REFERENCES catalog.works(work_key)
    );