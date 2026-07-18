CREATE TABLE IF NOT EXISTS catalog.authors_alternative_names
    (
        author_key TEXT NOT NULL,
        author_alternative_name TEXT NOT NULL,

        PRIMARY KEY (author_key, author_alternative_name),

        CONSTRAINT fk_authors_alternative_names_author_key
            FOREIGN KEY (author_key)
            REFERENCES catalog.authors(author_key)
    );