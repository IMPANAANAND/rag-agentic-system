CREATE DATABASE IF NOT EXISTS federal_register_db;
USE federal_register_db;

CREATE TABLE IF NOT EXISTS executive_orders (
    document_number VARCHAR(50) PRIMARY KEY,
    title TEXT,
    publication_date DATE,
    president VARCHAR(100),
    abstract TEXT,
    full_text_url TEXT
);