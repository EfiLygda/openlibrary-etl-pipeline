UPDATE
    reservations
SET
    fulfillment_loan_id = %(fulfillment_loan_id)s
WHERE
    reservation_id = %(reservation_id)s
RETURNING
    reservation_id;