INSERT INTO library.librarians (
    librarian_id,
    first_name,
    last_name,
    email,
    registered_at
)
VALUES (%(librarian_id)s, %(first_name)s, %(last_name)s, %(email)s, %(registered_at)s)
RETURNING librarian_id;