CREATE TABLE IF NOT EXISTS authors_works
    (
        author_key VARCHAR NOT NULL,
        work_key VARCHAR NOT NULL,

        PRIMARY KEY (author_key, work_key),

        CONSTRAINT fk_authors_works_author_key
            FOREIGN KEY (author_key)
            REFERENCES authors(author_key),
        CONSTRAINT fk_authors_works_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );