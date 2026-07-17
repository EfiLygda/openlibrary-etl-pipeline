CREATE TYPE
    loan_status AS ENUM (
            'ACTIVE',
            'RETURNED'
        );

CREATE TABLE IF NOT EXISTS loans (
    loan_id                 TEXT PRIMARY KEY,
    user_id                 TEXT NOT NULL,
    copy_id                 TEXT NOT NULL,

    borrow_date             TIMESTAMP,
    due_date                TIMESTAMP,
    return_date             TIMESTAMP DEFAULT NULL,

    renewal_count           INTEGER DEFAULT 0,
    status                  loan_status,
    loan_processed_by       TEXT,
    return_processed_by     TEXT,

    CONSTRAINT fk_loans_user_id
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_loans_copy_id
        FOREIGN KEY (copy_id)
        REFERENCES copies(copy_id),

    CONSTRAINT fk_loans_loan_processed_by
        FOREIGN KEY (loan_processed_by)
        REFERENCES librarians(librarian_id),

    CONSTRAINT fk_loans_return_processed_by
        FOREIGN KEY (return_processed_by)
        REFERENCES librarians(librarian_id)
);