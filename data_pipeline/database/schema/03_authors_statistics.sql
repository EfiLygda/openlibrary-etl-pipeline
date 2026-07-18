CREATE TABLE IF NOT EXISTS catalog.authors_statistics
        (
            author_key TEXT PRIMARY KEY,
            top_work TEXT,
            work_count INT,
            ratings_count_1 INT,
            ratings_count_2 INT,
            ratings_count_3 INT,
            ratings_count_4 INT,
            ratings_count_5 INT,
            readinglog_count INT,
            want_to_read_count INT,
            currently_reading_count INT,
            already_read_count INT,

            CONSTRAINT fk_authors_statistics_author_key
                FOREIGN KEY (author_key)
                REFERENCES catalog.authors(author_key)
        );