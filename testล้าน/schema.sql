CREATE TABLE IF NOT EXISTS clients (
    id TEXT PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS images (
    id BIGSERIAL PRIMARY KEY,
    client_id TEXT REFERENCES clients(id),
    url TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_images_client ON images (client_id, created_at DESC);

CREATE TABLE IF NOT EXISTS ai_tests (
    id BIGSERIAL PRIMARY KEY,
    image_id BIGINT REFERENCES images(id),
    label TEXT,
    confidence DOUBLE PRECISION,
    created_at TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX IF NOT EXISTS idx_ai_tests_image ON ai_tests (image_id, created_at DESC);
