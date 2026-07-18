 -- For get_publishing.sql
 CREATE INDEX IF NOT EXISTS idx_editions_publishing_edition_key
 ON editions_publishing (edition_key);