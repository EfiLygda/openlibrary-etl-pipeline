CREATE TYPE
    library.fine_status AS ENUM (
            'PAID',
            'UNPAID'
        );

CREATE TYPE
    library.fine_type AS ENUM (
        'OVERDUE',
        'LOST_COPY'
    );

CREATE TABLE IF NOT EXISTS library.fines (
    fine_id         TEXT PRIMARY KEY,
    loan_id         TEXT NOT NULL,

    overdue_days    INTEGER,
    amount          NUMERIC(8,2),

    issued_at       TIMESTAMP,
    paid_at         TIMESTAMP,

    status          library.fine_status,
    fine_type       library.fine_type NOT NULL,

    CONSTRAINT fk_fines_loan_id
        FOREIGN KEY (loan_id)
        REFERENCES library.loans(loan_id)
);