-- Trigram index via pg_trgm for search.sql
CREATE INDEX IF NOT EXISTS works_series_name_trgm_idx
ON works_series
USING gin (series_name gin_trgm_ops);