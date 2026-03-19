# Karoo Agriculture Capstone: Q4 Performance Report

## Project Overview
This repository contains the implementation of the Karoo Organics' automated quarterly performance report. The solution replaces manual Excel reporting by defining a relational database schema, importing data from CSVs, running analytical SQL queries, and utilizing a Python script for report automation.

## Project Structure
- `schema.sql`: Contains the DDL statements for creating the relational tables (`Suppliers`, `Orders`, `Sales_Targets`, `Certifications`, `Harvest_Log`) with constraints for referential integrity.
- `load_data.py`: A Python script containing DML operations. It connects to an SQLite database (`karoo.db`), creates the schema, loads the baseline CSV files (`suppliers.csv`, `orderss.csv`, `targets.csv`), and uses parameterized `INSERT` statements to load extra harvest and order test data.
- `analytics.sql`: Contains the SQL queries to analyze regional revenue vs. targets and calculate the top 3 suppliers per region using aggregate functions, `CASE` (implied by requirement or division), and window functions like `RANK() OVER (PARTITION BY ...)`.
- `generate_q4_report.py`: The final automation script that runs the SQL queries, prints a summary to the console, and exports the data to `q4_performance.csv`. Include typical defensive programming structures like `try...except...finally` block to handle DB errors.

## Design Choices & Implementation Details
- **Database Choice**: This capstone implements PostgreSQL using `psycopg2` as the database engine, as requested by the baseline guidelines. 
- **Data Insertion**: In `load_data.py`, I successfully use the `pandas` and `execute_values` approach to efficiently bulk-insert all the CSV data points and Python mock data correctly. 
- **Data Integrity**: DDL (`schema.sql`) sets up `FOREIGN KEY` constraints on table relationships so that rogue data cannot be inserted into the `Orders`, `Harvest_Log`, or `Certifications` table without a valid `supplier_id`. 
- **Analytics Design**: The main analytical queries efficiently group and join records, employing Common Table Expressions (CTEs) and Ranking functions (`RANK() OVER`) to pull top regional metrics.

## How to Run:
**Prerequisites**: Make sure PostgreSQL is running, and you have entered your `password` into the `DB_CONFIG` dictionary inside both `load_data.py` and `generate_q4_report.py`.

```bash
# 1. Initialize schema and load the data
python3 load_data.py

# 2. Generate the report and console summary
python3 generate_q4_report.py
```
After executing, the analytical results will be exported locally to `q4_performance.csv`.