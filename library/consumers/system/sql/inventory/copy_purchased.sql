INSERT INTO library.copies (
    copy_id,
    edition_key,
    status,
    registered_at
)
VALUES (%(copy_id)s, %(edition_key)s, %(status)s, %(registered_at)s)
RETURNING copy_id;