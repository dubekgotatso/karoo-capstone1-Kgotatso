-- Karoo Agriculture Capstone Project - PostgreSQL Database Schema

DROP TABLE IF EXISTS Harvest_Log, Certifications, Orders, Sales_Targets, Suppliers CASCADE;

-- Suppliers Table
CREATE TABLE Suppliers (
    supplier_id INTEGER PRIMARY KEY,
    farm_name VARCHAR(255) NOT NULL,
    region VARCHAR(100) NOT NULL
);

-- Orders Table
CREATE TABLE Orders (
    order_id INTEGER PRIMARY KEY,
    supplier_id INTEGER NOT NULL REFERENCES Suppliers(supplier_id),
    order_date DATE NOT NULL,
    total_price DECIMAL(12,2) NOT NULL
);

-- Sales Targets Table
CREATE TABLE Sales_Targets (
    region VARCHAR(100) NOT NULL,
    quarter VARCHAR(10) NOT NULL,
    target_amount DECIMAL(12,2) NOT NULL,
    PRIMARY KEY (region, quarter)
);

-- Certifications Table
CREATE TABLE Certifications (
    cert_id SERIAL PRIMARY KEY,
    supplier_id INTEGER NOT NULL REFERENCES Suppliers(supplier_id),
    cert_name VARCHAR(100) NOT NULL,
    issue_date DATE NOT NULL,
    valid_until DATE
);

-- Harvest Log Table
CREATE TABLE Harvest_Log (
    harvest_id SERIAL PRIMARY KEY,
    supplier_id INTEGER NOT NULL REFERENCES Suppliers(supplier_id),
    crop_type VARCHAR(100) NOT NULL,
    quantity_kg DECIMAL(10,2) NOT NULL,
    harvest_date DATE NOT NULL
);
