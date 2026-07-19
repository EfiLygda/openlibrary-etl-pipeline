INSERT INTO library.users (
    user_id,
    first_name,
    last_name,
    email,
    registered_at
)
VALUES (%(user_id)s, %(first_name)s, %(last_name)s, %(email)s, %(registered_at)s)
RETURNING user_id;