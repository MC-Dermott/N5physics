-- Run this in the Supabase SQL Editor (supabase.com → your project → SQL Editor)

CREATE TABLE users (
    id            UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    username      TEXT        UNIQUE NOT NULL,
    password_hash TEXT        NOT NULL,
    role          TEXT        NOT NULL DEFAULT 'student'
                              CHECK (role IN ('student', 'teacher')),
    created_at    TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE question_attempts (
    id            UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id       UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    qualification TEXT        NOT NULL,
    topic         TEXT        NOT NULL,
    question_type TEXT        NOT NULL,
    correct       BOOLEAN     NOT NULL,
    attempted_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE test_results (
    id            UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id       UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    qualification TEXT        NOT NULL,
    topic         TEXT        NOT NULL,
    question_type TEXT        NOT NULL,
    score         INTEGER     NOT NULL,
    total         INTEGER     NOT NULL,
    taken_at      TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON question_attempts (user_id);
CREATE INDEX ON test_results (user_id);

-- Per-question results from tests, with the specific mistake made (if any).
-- Run after the tables above.
CREATE TABLE test_question_attempts (
    id            UUID        DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id       UUID        NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    qualification TEXT        NOT NULL,
    topic         TEXT        NOT NULL,
    question_type TEXT        NOT NULL,
    correct       BOOLEAN     NOT NULL,
    mistake       TEXT,
    attempted_at  TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX ON test_question_attempts (user_id);

-- Disable RLS so the anon key can read/write all three tracking tables.
ALTER TABLE users                  DISABLE ROW LEVEL SECURITY;
ALTER TABLE question_attempts      DISABLE ROW LEVEL SECURITY;
ALTER TABLE test_results           DISABLE ROW LEVEL SECURITY;
ALTER TABLE test_question_attempts DISABLE ROW LEVEL SECURITY;
