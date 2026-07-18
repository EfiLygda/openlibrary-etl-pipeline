SELECT
    w.*
FROM
    catalog.works AS w
    INNER JOIN
    unnest(                                     -- 2. unnest converts list of keys to table with one column of the keys
        %(filter_key)s::text[]                  -- 1. ::text[] converts list of key to SQL array {'key1', 'key2', ...}
    ) WITH ORDINALITY AS k(work_key, ord)       -- 3. ORDINALITY adds a new column with order values 1,2,...
                                                -- 4. k(work_key, ord) -> renames table to k and columns to work_key, ord
    ON w.work_key = k.work_key
ORDER BY                                        -- Keep original order
    k.ord
LIMIT
    %(limit)s
OFFSET
    %(offset)s