CREATE TABLE IF NOT EXISTS authors_statistics
        (
            author_key VARCHAR PRIMARY KEY,
            top_work VARCHAR,
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
                REFERENCES authors(author_key)
        );