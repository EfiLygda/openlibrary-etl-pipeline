-- Trigram index via pg_trgm for search.sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX IF NOT EXISTS works_places_place_trgm_idx
ON works_places
USING gin (place gin_trgm_ops);