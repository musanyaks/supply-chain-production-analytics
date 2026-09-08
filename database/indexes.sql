-- indexes.sql
CREATE INDEX idx_inventory_product ON inventory(product_id);
CREATE INDEX idx_procurement_product ON procurement(product_id);
CREATE INDEX idx_procurement_supplier ON procurement(supplier_id);
CREATE INDEX idx_production_product ON production(product_id);
CREATE INDEX idx_sales_product ON sales(product_id);
CREATE INDEX idx_sales_date ON sales(sale_date);