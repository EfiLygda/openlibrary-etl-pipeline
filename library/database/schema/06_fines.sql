CREATE TYPE
    fine_status AS ENUM (
            'PAID',
            'UNPAID'
        );

CREATE TABLE IF NOT EXISTS fines (
    fine_id         TEXT PRIMARY KEY,
    loan_id         TEXT NOT NULL,

    overdue_days    INTEGER,
    amount          NUMERIC(8,2),

    issued_at       TIMESTAMP,
    paid_at         TIMESTAMP,

    status          fine_status,

    CONSTRAINT fk_fines_loan_id
        FOREIGN KEY (loan_id)
        REFERENCES loans(loan_id)
);