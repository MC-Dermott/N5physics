-- Batches: assignments made by one tracker import share a batch name, so the Track page shows the whole
-- import as a single entry instead of one per set of focus topics. NULL = a standalone assignment.
-- Run once in the Supabase SQL Editor.

ALTER TABLE assignments ADD COLUMN IF NOT EXISTS batch TEXT;

-- Tag the 26 Oct 2026 tracker import (the class-wide "S3 Motion" assignment is not part of it).
UPDATE assignments SET batch = 'Focus topics, 26 Oct 2026'
WHERE batch IS NULL AND title LIKE 'Focus topics —%' AND created_at::date = '2026-10-26';
