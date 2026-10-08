-- Assignments: a teacher picks topics (items), a pass mark and a due date, and targets whole
-- classes (class_code) and/or individual pupils. A pupil's work counts only if the test was
-- taken through the assignment (test_results.assignment_id), so completion is verifiable.

CREATE TABLE IF NOT EXISTS assignments (
    id          UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    title       TEXT        NOT NULL,
    created_by  UUID        REFERENCES users(id) ON DELETE SET NULL,
    created_at  TIMESTAMPTZ DEFAULT NOW(),
    due_date    DATE,
    pass_pct    INTEGER     NOT NULL DEFAULT 60 CHECK (pass_pct BETWEEN 0 AND 100)
);

CREATE TABLE IF NOT EXISTS assignment_items (
    id            UUID    DEFAULT gen_random_uuid() PRIMARY KEY,
    assignment_id UUID    NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    position      INTEGER NOT NULL DEFAULT 0,
    qualification TEXT    NOT NULL,
    topic         TEXT    NOT NULL,
    question_type TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS assignment_targets (
    id            UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    assignment_id UUID NOT NULL REFERENCES assignments(id) ON DELETE CASCADE,
    class_code    TEXT,
    user_id       UUID REFERENCES users(id) ON DELETE CASCADE,
    CHECK ((class_code IS NOT NULL) <> (user_id IS NOT NULL))
);

ALTER TABLE test_results ADD COLUMN IF NOT EXISTS assignment_id UUID
    REFERENCES assignments(id) ON DELETE SET NULL;

CREATE INDEX IF NOT EXISTS assignment_items_assignment_idx   ON assignment_items (assignment_id);
CREATE INDEX IF NOT EXISTS assignment_targets_assignment_idx ON assignment_targets (assignment_id);
CREATE INDEX IF NOT EXISTS assignment_targets_user_idx       ON assignment_targets (user_id);
CREATE INDEX IF NOT EXISTS test_results_assignment_idx       ON test_results (assignment_id);

ALTER TABLE assignments        ENABLE ROW LEVEL SECURITY;
ALTER TABLE assignment_items   ENABLE ROW LEVEL SECURITY;
ALTER TABLE assignment_targets ENABLE ROW LEVEL SECURITY;
