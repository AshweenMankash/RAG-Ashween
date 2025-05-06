CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE vectors (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id TEXT NOT NULL,
    content TEXT,
    metadata JSONB,
    embedding VECTOR(384)
);
