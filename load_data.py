import psycopg2
import pandas as pd
from psycopg2.extras import execute_values

# Replace with your actual PostgreSQL password
DB_CONFIG = {
    "host": "localhost",
    "database": "karoo_agriculture",
    "user": "postgres",
    "password": ""
}

def create_database():
    try:
        # Connect to default 'postgres' db to create the new one
        conn = psycopg2.connect(host=DB_CONFIG['host'], database="postgres", user=DB_CONFIG['user'], password=DB_CONFIG['password'])
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{DB_CONFIG['database']}'")
        exists = cur.fetchone()
        if not exists:
            print(f"Database {DB_CONFIG['database']} does not exist. Creating it now...")
            cur.execute(f"CREATE DATABASE {DB_CONFIG['database']}")
        cur.close()
        conn.close()
    except Exception as e:
        print(f"Could not check/create database: {e}")

def run_sql(query):
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    cur.execute(query)
    conn.commit()
    cur.close()
    conn.close()

def load_data():
    try:
        # 0. Ensure database exists
        create_database()

        # 1. Provide the basic schema
        print("Creating schema...")
        with open('schema.sql', 'r') as f:
            schema_sql = f.read()
        run_sql(schema_sql)
        print("Schema created successfully!")

        print("Connecting to load data...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        # 2. Load Suppliers
        suppliers_df = pd.read_csv('suppliers.csv')
        suppliers_vals = [tuple(x) for x in suppliers_df.to_numpy()]
        execute_values(cur, 
            "INSERT INTO Suppliers (supplier_id, farm_name, region) VALUES %s ON CONFLICT (supplier_id) DO NOTHING", 
            suppliers_vals
        )

        # 3. Load Orders
        orders_df = pd.read_csv('orderss.csv')
        orders_vals = [tuple(x) for x in orders_df.to_numpy()]
        execute_values(cur, 
            "INSERT INTO Orders (order_id, supplier_id, order_date, total_price) VALUES %s ON CONFLICT (order_id) DO NOTHING", 
            orders_vals
        )

        # 4. Load Targets
        targets_df = pd.read_csv('targets.csv')
        targets_vals = [tuple(x) for x in targets_df.to_numpy()]
        execute_values(cur, 
            "INSERT INTO Sales_Targets (region, quarter, target_amount) VALUES %s ON CONFLICT (region, quarter) DO NOTHING", 
            targets_vals
        )

        # 5. Insert 5 additional harvest records
        harvest_records = [
            (1, 'Apples', 1200.50, '2025-10-10'),
            (2, 'Oranges', 800.00, '2025-10-15'),
            (3, 'Wool', 500.25, '2025-11-20'),
            (4, 'Grapes', 2300.75, '2025-12-05'),
            (5, 'Olives', 400.00, '2025-12-18')
        ]
        execute_values(cur,
            "INSERT INTO Harvest_Log (supplier_id, crop_type, quantity_kg, harvest_date) VALUES %s",
            harvest_records
        )

        # 6. Insert 4 additional orders for Q4 2025
        additional_orders = [
            (12, 1, '2025-12-20', 3000.00),
            (13, 3, '2025-12-22', 1500.00),
            (14, 4, '2025-12-28', 8500.00),
            (15, 6, '2025-12-30', 4200.00)
        ]
        execute_values(cur,
            "INSERT INTO Orders (order_id, supplier_id, order_date, total_price) VALUES %s ON CONFLICT (order_id) DO NOTHING",
            additional_orders
        )

        conn.commit()
        print("Data loaded successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")
        if 'conn' in locals() and conn:
            conn.rollback()
    finally:
        if 'cur' in locals() and cur:
            cur.close()
        if 'conn' in locals() and conn:
            conn.close()

if __name__ == "__main__":
    load_data()
