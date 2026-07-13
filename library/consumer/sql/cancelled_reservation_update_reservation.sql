UPDATE
    reservations
SET
    status = %(status)s,
    cancelled_at = %(cancelled_at)s
WHERE
    reservation_id = %(reservation_id)s
RETURNING
    reservation_id;