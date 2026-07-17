CREATE TYPE
    reservation_status AS ENUM (
            'ACTIVE',
            'FULFILLED',
            'CANCELLED'
        );

CREATE TABLE IF NOT EXISTS reservations (
    reservation_id      TEXT PRIMARY KEY,
    user_id             TEXT NOT NULL,
    copy_id             TEXT NOT NULL,

    reserved_at         TIMESTAMP,

    fulfilled_at        TIMESTAMP,
    fulfillment_loan_id TEXT,
    cancelled_at        TIMESTAMP,
    status              reservation_status,

    CONSTRAINT fk_reservations_user_id
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_reservations_copy_id
        FOREIGN KEY (copy_id)
        REFERENCES copies(copy_id),

    CONSTRAINT fk_reservations_fulfillment_loan_id
    FOREIGN KEY (fulfillment_loan_id)
    REFERENCES loans(loan_id)
);