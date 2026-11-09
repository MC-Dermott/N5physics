-- Marks whether a revision guide row comes from the pupil's own marks ('own') or the class's results ('class'),
-- used when a pupil missed a homework or assessment. Run once in the Supabase SQL Editor, before the next sync.
ALTER TABLE revision_guide ADD COLUMN IF NOT EXISTS source TEXT NOT NULL DEFAULT 'own';
