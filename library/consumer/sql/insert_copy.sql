INSERT INTO copies (
    edition_key,
    status,
    registered_at
)
VALUES (%(edition_key)s, %(status)s, %(registered_at)s)
RETURNING copy_id;