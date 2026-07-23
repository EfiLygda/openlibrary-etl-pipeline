UPDATE
    library.loans
SET
    status = 'LOST'
WHERE
    loan_id = %(loan_id)s;

UPDATE
    library.copies
SET
    status = 'WITHDRAWN',
    withdrawal_reason = 'LOST',
    withdrawn_at = %(withdrawn_at)s
WHERE
    copy_id = %(copy_id)s;