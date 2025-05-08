CREATE TABLE heart_beats (
    id SERIAL PRIMARY KEY,
    customer_id INT NOT NULL,
    timestamp TIMESTAMPTZ NOT NULL,
    heart_rate INT NOT NULL
);
CREATE INDEX idx_timestamp ON heart_beats(timestamp);
