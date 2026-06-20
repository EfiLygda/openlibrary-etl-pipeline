-- Trigram index via pg_trgm for search.sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX IF NOT EXISTS works_subjects_subject_trgm_idx
ON works_subjects
USING gin (subject gin_trgm_ops);