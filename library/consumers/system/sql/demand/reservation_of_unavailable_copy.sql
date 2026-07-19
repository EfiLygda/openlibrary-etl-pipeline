INSERT INTO library.reservations (
    reservation_id,
    user_id,
    copy_id,
    reserved_at,
    fulfilled_at,
    cancelled_at,
    status
)
VALUES (
    %(reservation_id)s,
    %(user_id)s,
    %(copy_id)s,
    %(reserved_at)s,
    %(fulfilled_at)s,
    %(cancelled_at)s,
    %(status)s
)
RETURNING reservation_id;