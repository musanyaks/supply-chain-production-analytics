-- views.sql
CREATE OR REPLACE VIEW vw_inventory_status AS
SELECT 
    p.sku, 
    p.name, 
    i.quantity, 
    i.safety_stock, 
    i.reorder_point,
    CASE 
        WHEN i.quantity <= i.safety_stock THEN 'CRITICAL'
        WHEN i.quantity <= i.reorder_point THEN 'WARNING'
        ELSE 'OPTIMAL'
    END AS status
FROM products p
JOIN inventory i ON p.id = i.product_id;

CREATE OR REPLACE VIEW vw_supplier_performance AS
SELECT 
    s.name AS supplier,
    COUNT(p.id) AS total_orders,
    AVG(CASE WHEN p.status = 'RECEIVED' THEN 1 ELSE 0 END) AS fulfillment_rate,
    AVG(s.lead_time_days) AS avg_lead_time
FROM suppliers s
LEFT JOIN procurement p ON s.id = p.supplier_id
GROUP BY s.name;