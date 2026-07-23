INSERT INTO library.fines (
    fine_id,
    loan_id,
    overdue_days,
    amount,
    issued_at,
    status,
    fine_type
)
VALUES (
    %(fine_id)s,
    %(loan_id)s,
    %(overdue_days)s,
    %(amount)s,
    %(issued_at)s,
    %(status)s,
    %(fine_type)s
)
RETURNING fine_id;