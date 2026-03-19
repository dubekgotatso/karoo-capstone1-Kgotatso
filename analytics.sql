-- Question 1: Regional performance against sales targets
-- Returns: region, actual revenue, target amount, % of target
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

-- Question 2: Top 3 suppliers per region by revenue
-- Returns: region, farm_name, total_revenue, regional_rank
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
SELECT 
    region, 
    farm_name, 
    total_revenue, 
    regional_rank
FROM RankedSuppliers
WHERE regional_rank <= 3
ORDER BY region ASC, regional_rank ASC;
