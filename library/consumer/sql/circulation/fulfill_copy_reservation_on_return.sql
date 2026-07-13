UPDATE
    reservations
SET
    status = 'FULFILLED',
    fulfilled_at = %(fulfilled_at)s
WHERE
    reservation_id = %(reservation_id)s
RETURNING
    reservation_id;