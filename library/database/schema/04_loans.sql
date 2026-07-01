CREATE TABLE IF NOT EXISTS loans (
    loan_id        SERIAL PRIMARY KEY,
    user_id        SERIAL NOT NULL,
    copy_id        SERIAL NOT NULL,

    borrow_date    TIMESTAMP,
    due_date       TIMESTAMP,
    return_date    TIMESTAMP DEFAULT NULL,

    renewal_count  INTEGER DEFAULT 0,
    status         TEXT,
    processed_by   INT,

    CONSTRAINT fk_loans_user_id
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_loans_copy_id
        FOREIGN KEY (copy_id)
        REFERENCES copies(copy_id),

    CONSTRAINT fk_loans_processed_by
        FOREIGN KEY (processed_by)
        REFERENCES librarians(librarian_id)
);