-- Trigram index via pg_trgm for search.sql
CREATE INDEX IF NOT EXISTS authors_alternative_names_trgm_idx
ON authors_alternative_names
USING gin (author_alternative_name gin_trgm_ops);