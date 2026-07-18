 -- For get_contributors.sql
 CREATE INDEX IF NOT EXISTS idx_editions_contributors_edition_key
 ON editions_contributors (edition_key);