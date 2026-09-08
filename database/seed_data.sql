-- seed_data.sql
INSERT INTO products (sku, name, type, unit_cost, holding_cost) VALUES 
('WIDGET-01', 'Steel Widget', 'RAW_MATERIAL', 5.00, 1.20),
('GADGET-01', 'Assembled Gadget', 'FINISHED_GOOD', 25.00, 3.50),
('SCREW-01', '1mm Screw', 'RAW_MATERIAL', 0.10, 0.02);

INSERT INTO suppliers (name, contact_email, lead_time_days, risk_score) VALUES 
('Acme Corp', 'sales@acme.com', 7, 0.15),
('Global Materials', 'contact@globalm.com', 14, 0.35);

INSERT INTO customers (name, region) VALUES 
('Tech Retailer', 'North America'),
('Europe Distros', 'Europe');

-- Set initial inventory for WIDGET-01
INSERT INTO inventory (product_id, quantity, safety_stock, reorder_point) 
SELECT id, 45, 50, 100 FROM products WHERE sku = 'WIDGET-01';

-- Set initial inventory for GADGET-01
INSERT INTO inventory (product_id, quantity, safety_stock, reorder_point) 
SELECT id, 120, 30, 80 FROM products WHERE sku = 'GADGET-01';