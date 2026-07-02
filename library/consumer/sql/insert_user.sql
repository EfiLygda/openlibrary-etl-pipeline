INSERT INTO users (
    first_name,
    last_name,
    email,
    registered_at
)
VALUES (%(first_name)s, %(last_name)s, %(email)s, %(registered_at)s)
RETURNING user_id;