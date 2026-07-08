UPDATE
    loans
SET
    status = 'RETURNED',
    return_date = %(return_date)s
WHERE
    loan_id = %(loan_id)s
RETURNING
    loan_id;

UPDATE
    copies
SET
    status = %(status)s
WHERE
    copy_id = %(copy_id)s
RETURNING
    copy_id;