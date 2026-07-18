-- Trigram index via pg_trgm for search.sql
CREATE INDEX IF NOT EXISTS works_time_periods_trgm_idx
ON catalog.works_time_periods
USING gin (time_period gin_trgm_ops);