CREATE TABLE transactions (
    transaction_id SERIAL PRIMARY KEY,
    transaction_type transaction_type_enum NOT NULL,
    transaction_date TIMESTAMP,
    asset_name VARCHAR(255) not null,
    ticker VARCHAR(10) NOT NULL,
    units numeric(12,4) not null,
    buy_price NUMERIC(12, 4) NOT NULL,
    total_transaction_amount numeric(12,4) NOT NULL,
    realized_profit NUMERIC(12, 4)  -- NULL for BUYs, calculated for SELLs
    );