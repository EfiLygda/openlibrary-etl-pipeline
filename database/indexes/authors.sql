-- Trigram index via pg_trgm for search.sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX IF NOT EXISTS authors_author_name_trgm_idx
ON authors
USING gin (author_name gin_trgm_ops);