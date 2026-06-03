CREATE TABLE IF NOT EXISTS works_availability
    (
        work_key VARCHAR PRIMARY KEY,
        ebook_access VARCHAR,
        has_fulltext BOOL,
        has_public_scan BOOL,

        CONSTRAINT fk_works_availability_work_key
            FOREIGN KEY (work_key)
            REFERENCES works(work_key)
    );