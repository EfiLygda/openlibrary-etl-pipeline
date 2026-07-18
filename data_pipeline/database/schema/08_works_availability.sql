CREATE TABLE IF NOT EXISTS catalog.works_availability
    (
        work_key TEXT PRIMARY KEY,
        ebook_access TEXT,
        has_fulltext BOOL,
        has_public_scan BOOL,

        CONSTRAINT fk_works_availability_work_key
            FOREIGN KEY (work_key)
            REFERENCES catalog.works(work_key)
    );