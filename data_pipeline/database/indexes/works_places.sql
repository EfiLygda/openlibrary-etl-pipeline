-- Trigram index via pg_trgm for search.sql
CREATE INDEX IF NOT EXISTS works_places_place_trgm_idx
ON catalog.works_places
USING gin (place gin_trgm_ops);