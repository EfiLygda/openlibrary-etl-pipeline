-- Trigram index via pg_trgm for search.sql
CREATE INDEX IF NOT EXISTS works_subjects_subject_trgm_idx
ON works_subjects
USING gin (subject gin_trgm_ops);