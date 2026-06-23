SELECT
    a.*
FROM
    authors AS a
    INNER JOIN
    unnest(                                     -- 2. unnest converts list of keys to table with one column of the keys
        %(filter_key)s::text[]                  -- 1. ::text[] converts list of key to SQL array {'key1', 'key2', ...}
    ) WITH ORDINALITY AS k(author_key, ord)     -- 3. ORDINALITY adds a new column with order values 1,2,...
                                                -- 4. k(author_key, ord) -> renames table to k and columns to author_key, ord
    ON a.author_key = k.author_key
ORDER BY                                        -- Keep original order
    k.ord
LIMIT
    %(limit)s
OFFSET
    %(offset)s