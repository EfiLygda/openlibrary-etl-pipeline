-- Insert new loan record
INSERT INTO loans (
    loan_id,
    user_id,
    copy_id,

    borrow_date,
    due_date,
    return_date,

    renewal_count,
    status,
    processed_by
)
VALUES (
    %(loan_id)s, %(user_id)s, %(copy_id)s,
    %(borrow_date)s, %(due_date)s, %(return_date)s,
    %(renewal_count)s, %(status)s, %(processed_by)s
)
RETURNING loan_id;

-- Update copy's status to 'UNAVAILABLE'
UPDATE
    copies
SET
    status = 'UNAVAILABLE'
WHERE
    copy_id = %(copy_id)s;