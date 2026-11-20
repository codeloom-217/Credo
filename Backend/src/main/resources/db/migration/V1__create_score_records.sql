
CREATE TABLE score_records (
    id BIGSERIAL PRIMARY KEY,
    customer_id VARCHAR(100) NOT NULL,
    credo_score INTEGER,
    risk_band VARCHAR(20),
    predicted_outcome INTEGER,
    predicted_probability DOUBLE PRECISION,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
);
