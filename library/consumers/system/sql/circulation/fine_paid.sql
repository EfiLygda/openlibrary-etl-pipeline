UPDATE
    library.fines
SET
    paid_at = %(paid_at)s,
    status = %(status)s
WHERE
    fine_id = %(fine_id)s
RETURNING fine_id;