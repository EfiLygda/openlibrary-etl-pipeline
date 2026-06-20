 -- For get_editions.sql
 CREATE INDEX IF NOT EXISTS idx_editions_work_key
 ON editions (work_key);

-- Trigram indexes via pg_trgm for search.sql
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX IF NOT EXISTS editions_title_trgm_idx
ON editions
USING gin (title gin_trgm_ops);

CREATE INDEX IF NOT EXISTS editions_subtitle_trgm_idx
ON editions
USING gin (subtitle gin_trgm_ops);