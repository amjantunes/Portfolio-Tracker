### 📈 Portfolio Tracker (PTR)
An automated financial asset monitoring system

This project was born out of the need to centralize the tracking of investments made across different stock exchanges and assets, allowing for the visualization of real Profit/Loss in Euros, regardless of the assets' original currency.

#### 🚀 Key Features
(TODO)Automated FX Sync: Daily GitHub Actions workflow to fetch and store EUR/USD exchange rates.

Real-time Market Data: Integrated with the Yahoo Finance API for stock and ETF price tracking

Dynamic Profit Calculation: Automatic conversion based on the exact exchange rate of the transaction date.

#### 🛠️ Tech Stack
Language: Python 3.x

Database: PostgreSQL

Core Libraries: yfinance, pandas, psycopg2, python-dotenv

TODO: Infrastructure: GitHub Actions (CI/CD for data orchestration)

#### 🏗️ Data Architecture
The system uses a Lookup Table approach for currency exchange:

TODO: A daily cron job triggers via GitHub Actions.

The Python script fetches the latest closing rates and performs an UPSERT into the exchange_rates table.

SQL queries perform a JOIN between user transactions and historical rates to reflect the real-time Euro value of the portfolio.