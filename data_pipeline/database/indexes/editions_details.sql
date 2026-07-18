 -- For get_details.sql
 CREATE INDEX IF NOT EXISTS idx_editions_details_edition_key
 ON catalog.editions_details (edition_key);