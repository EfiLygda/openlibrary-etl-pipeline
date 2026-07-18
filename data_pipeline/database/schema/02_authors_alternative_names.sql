CREATE TABLE IF NOT EXISTS authors_alternative_names
    (
        author_key VARCHAR NOT NULL,
        author_alternative_name VARCHAR NOT NULL,

        PRIMARY KEY (author_key, author_alternative_name),

        CONSTRAINT fk_authors_alternative_names_author_key
            FOREIGN KEY (author_key)
            REFERENCES authors(author_key)
    );