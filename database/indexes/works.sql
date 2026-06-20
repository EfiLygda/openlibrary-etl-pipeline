-- Trigram indexes via pg_trgm for search.sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX IF NOT EXISTS works_title_trgm_idx
ON works
USING gin (title gin_trgm_ops);

CREATE INDEX IF NOT EXISTS works_subtitle_trgm_idx
ON works
USING gin (subtitle gin_trgm_ops);