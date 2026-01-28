
CREATE TABLE exchange_rates (
    rate_date DATE PRIMARY KEY,
    currency_pair VARCHAR(6) DEFAULT 'EURUSD',
    rate NUMERIC(12, 6) NOT NULL
);