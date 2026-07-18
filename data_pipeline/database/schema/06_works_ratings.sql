CREATE TABLE IF NOT EXISTS catalog.works_ratings
    (
        work_key TEXT PRIMARY KEY,
        ratings_count_1 INT,
        ratings_count_2 INT,
        ratings_count_3 INT,
        ratings_count_4 INT,
        ratings_count_5 INT,

        CONSTRAINT fk_works_ratings_work_key
            FOREIGN KEY (work_key)
            REFERENCES catalog.works(work_key)
    );