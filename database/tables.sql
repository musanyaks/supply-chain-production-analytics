-- tables.sql
CREATE TABLE products (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sku VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) CHECK (type IN ('RAW_MATERIAL', 'FINISHED_GOOD')),
    unit_cost DECIMAL(10, 2) NOT NULL,
    holding_cost DECIMAL(10, 2) DEFAULT 0.00
);

CREATE TABLE suppliers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    contact_email VARCHAR(255),
    lead_time_days INT DEFAULT 0,
    risk_score DECIMAL(3, 2) DEFAULT 0.00
);

CREATE TABLE customers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    region VARCHAR(100)
);

CREATE TABLE inventory (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES products(id) ON DELETE CASCADE,
    quantity INT DEFAULT 0,
    safety_stock INT DEFAULT 0,
    reorder_point INT DEFAULT 0,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE procurement (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES products(id),
    supplier_id UUID REFERENCES suppliers(id),
    po_number VARCHAR(50),
    quantity INT NOT NULL,
    order_date DATE,
    expected_delivery DATE,
    status VARCHAR(50) DEFAULT 'PENDING'
);

CREATE TABLE production (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES products(id),
    production_date DATE,
    quantity_planned INT,
    quantity_produced INT DEFAULT 0,
    downtime_hours DECIMAL(5, 2) DEFAULT 0.00
);

CREATE TABLE sales (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    product_id UUID REFERENCES products(id),
    customer_id UUID REFERENCES customers(id),
    sale_date DATE,
    quantity INT,
    unit_price DECIMAL(10, 2)
);

CREATE TABLE deliveries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    sale_id UUID REFERENCES sales(id),
    delivery_date DATE,
    status VARCHAR(50) DEFAULT 'PENDING',
    shipping_cost DECIMAL(10, 2)
);