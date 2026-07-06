CREATE TABLE IF NOT EXISTS reservations (
    reservation_id    TEXT PRIMARY KEY,
    user_id           TEXT NOT NULL,
    copy_id           TEXT NOT NULL,

    reserved_at       TIMESTAMP,

    fulfilled_at      TIMESTAMP,
    cancelled_at      TIMESTAMP,
    status            TEXT,

    CONSTRAINT fk_reservations_user_id
        FOREIGN KEY (user_id)
        REFERENCES users(user_id),

    CONSTRAINT fk_reservations_copy_id
        FOREIGN KEY (copy_id)
        REFERENCES copies(copy_id)
);