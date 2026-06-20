-- Trigram index via pg_trgm for search.sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX IF NOT EXISTS works_people_person_trgm_idx
ON works_people
USING gin (person gin_trgm_ops);