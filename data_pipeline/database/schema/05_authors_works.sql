CREATE TABLE IF NOT EXISTS catalog.authors_works
    (
        author_key TEXT NOT NULL,
        work_key TEXT NOT NULL,

        PRIMARY KEY (author_key, work_key),

        CONSTRAINT fk_authors_works_author_key
            FOREIGN KEY (author_key)
            REFERENCES catalog.authors(author_key),
        CONSTRAINT fk_authors_works_work_key
            FOREIGN KEY (work_key)
            REFERENCES catalog.works(work_key)
    );