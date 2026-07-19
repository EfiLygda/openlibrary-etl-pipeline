UPDATE
    library.loans
SET
    renewal_count = 1,
    due_date = %(new_due_date)s
WHERE
    loan_id = %(loan_id)s
RETURNING loan_id;