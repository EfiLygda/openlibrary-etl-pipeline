-- Trigram index via pg_trgm for search.sql
CREATE INDEX IF NOT EXISTS works_people_person_trgm_idx
ON works_people
USING gin (person gin_trgm_ops);