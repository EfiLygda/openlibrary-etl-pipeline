CREATE TYPE
    library.reservation_status AS ENUM (
            'ACTIVE',
            'FULFILLED',
            'CANCELLED'
        );

CREATE TABLE IF NOT EXISTS library.reservations (
    reservation_id      TEXT PRIMARY KEY,
    user_id             TEXT NOT NULL,
    copy_id             TEXT NOT NULL,

    reserved_at         TIMESTAMP,

    fulfilled_at        TIMESTAMP,
    fulfillment_loan_id TEXT,
    cancelled_at        TIMESTAMP,
    status              library.reservation_status,

    CONSTRAINT fk_reservations_user_id
        FOREIGN KEY (user_id)
        REFERENCES library.users(user_id),

    CONSTRAINT fk_reservations_copy_id
        FOREIGN KEY (copy_id)
        REFERENCES library.copies(copy_id),

    CONSTRAINT fk_reservations_fulfillment_loan_id
    FOREIGN KEY (fulfillment_loan_id)
    REFERENCES library.loans(loan_id)
);