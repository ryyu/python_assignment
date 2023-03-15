CREATE DATABASE IF NOT EXISTS financial_data;

CREATE TABLE IF NOT EXISTS company_financial_data (
    Entry_ID INT AUTO_INCREMENT PRIMARY KEY, 
    symbol VARCHAR(50),
    entry_date DATE, 
    open_price DECIMAL(5,2), 
    close_price DECIMAL(5,2), 
    volume INTEGER,
    UNIQUE(entry_date, symbol)
);
