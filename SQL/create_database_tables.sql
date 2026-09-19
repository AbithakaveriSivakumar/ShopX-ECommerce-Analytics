-- =========================================================
-- ADMM Case Study - ShopX E-Commerce Analytics
-- Database and Table Creation
-- =========================================================

-- Create database
CREATE DATABASE IF NOT EXISTS shopx_dw;

USE shopx_dw;


-- =========================================================
-- 1. Customers Table
-- Source: KNA1
-- =========================================================

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(50) PRIMARY KEY,
    customer_name VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100)
);


-- =========================================================
-- 2. Carriers Table
-- Source: LFA1
-- =========================================================

CREATE TABLE IF NOT EXISTS carriers (
    carrier_id VARCHAR(50) PRIMARY KEY,
    carrier_name VARCHAR(255)
);


-- =========================================================
-- 3. Orders Table
-- Source: VBAK
-- =========================================================

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(50) PRIMARY KEY,
    customer_id VARCHAR(50),
    order_date DATE,

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);


-- =========================================================
-- 4. Order Items Table
-- Source: VBAP
-- =========================================================

CREATE TABLE IF NOT EXISTS order_items (
    order_id VARCHAR(50),
    item_id VARCHAR(50),
    material_id VARCHAR(50),
    quantity DECIMAL(15,2),

    PRIMARY KEY (order_id, item_id),

    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


-- =========================================================
-- 5. Shipments Table
-- Source: VTTK / VTTP
-- =========================================================

CREATE TABLE IF NOT EXISTS shipments (
    shipment_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50),
    carrier VARCHAR(100),
    shipment_date DATE,
    order_processing_days DECIMAL(10,2),

    CONSTRAINT fk_shipments_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)
);


-- =========================================================
-- 6. Shipment Items Table
-- Source: VTTP / LIPS
-- =========================================================

CREATE TABLE IF NOT EXISTS shipment_items (
    shipment_id VARCHAR(50),
    item_id VARCHAR(50),
    delivery_id VARCHAR(50),

    PRIMARY KEY (shipment_id, item_id),

    CONSTRAINT fk_shipment_items_shipment
        FOREIGN KEY (shipment_id)
        REFERENCES shipments(shipment_id)
);


-- =========================================================
-- 7. Delivery Analytics Table
-- =========================================================

CREATE TABLE IF NOT EXISTS delivery_analytics (
    delivery_id VARCHAR(50) PRIMARY KEY,
    order_id VARCHAR(50),
    shipment_id VARCHAR(50),
    actual_delivery_date DATE,
    expected_delivery_date DATE,
    delivery_delay DECIMAL(10,2),
    delay_reason VARCHAR(255),
    on_time BOOLEAN,

    CONSTRAINT fk_delivery_order
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    CONSTRAINT fk_delivery_shipment
        FOREIGN KEY (shipment_id)
        REFERENCES shipments(shipment_id)
);