import psycopg2
import csv

DB_CONFIG = {
    "host": "localhost",
    "database": "karoo_agriculture",
    "user": "postgres",
    "password": ""
}

def generate_report():
    conn = None
    try:
        print("Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # Query 1: Regional Performance
        print("Executing Query 1 (Regional Performance)...")
        query1 = """
        SELECT 
            s.region,
            SUM(o.total_price) AS actual_revenue,
            t.target_amount,
            ROUND((SUM(o.total_price) * 100.0) / t.target_amount, 2) AS percent_of_target
        FROM Suppliers s
        JOIN Orders o ON s.supplier_id = o.supplier_id
        JOIN Sales_Targets t ON s.region = t.region AND t.quarter = '2025-Q4'
        WHERE o.order_date >= '2025-10-01' AND o.order_date <= '2025-12-31'
        GROUP BY s.region, t.target_amount;
        """
        cursor.execute(query1)
        performance_results = cursor.fetchall()
        
        print("\n--- Q4 REGIONAL PERFORMANCE ---\n")
        print(f"{'Region':<20} | {'Actual Revenue':<15} | {'Target Amount':<15} | {'% of Target':<15}")
        print("-" * 75)
        for row in performance_results:
            print(f"{row[0]:<20} | R{row[1]:<14.2f} | R{row[2]:<14.2f} | {row[3]:<14}%")

        # Query 2: Top Suppliers
        print("\nExecuting Query 2 (Top 3 Suppliers per Region)...")
        query2 = """
        WITH SupplierRevenue AS (
            SELECT 
                s.region, 
                s.farm_name, 
                SUM(o.total_price) AS total_revenue
            FROM Suppliers s
            JOIN Orders o ON s.supplier_id = o.supplier_id
            WHERE o.order_date >= '2025-10-01' AND o.order_date <= '2025-12-31'
            GROUP BY s.supplier_id, s.region, s.farm_name
        ),
        RankedSuppliers AS (
            SELECT 
                region, 
                farm_name, 
                total_revenue,
                RANK() OVER (
                    PARTITION BY region 
                    ORDER BY total_revenue DESC
                ) AS regional_rank
            FROM SupplierRevenue
        )
        SELECT region, farm_name, total_revenue, regional_rank
        FROM RankedSuppliers
        WHERE regional_rank <= 3
        ORDER BY region ASC, regional_rank ASC;
        """
        cursor.execute(query2)
        ranking_results = cursor.fetchall()

        print("\n--- TOP 3 SUPPLIERS PER REGION ---\n")
        print(f"{'Region':<20} | {'Farm Name':<30} | {'Total Revenue':<15} | {'Rank'}")
        print("-" * 80)
        for row in ranking_results:
            print(f"{row[0]:<20} | {row[1]:<30} | R{row[2]:<14.2f} | {row[3]}")

        # Save to CSV
        print("\nSaving results to q4_performance.csv...")
        with open('q4_performance.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Write Query 1
            writer.writerow(['Regional Performance vs Target'])
            writer.writerow(['Region', 'Actual Revenue', 'Target Amount', '% of Target'])
            writer.writerows(performance_results)
            
            writer.writerow([]) # Empty row for spacing
            
            # Write Query 2
            writer.writerow(['Top 3 Suppliers per Region'])
            writer.writerow(['Region', 'Farm Name', 'Total Revenue', 'Rank'])
            writer.writerows(ranking_results)
            
        print("Success! Report saved.")

    except psycopg2.Error as e:
        print(f"Database error occurred: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    generate_report()
