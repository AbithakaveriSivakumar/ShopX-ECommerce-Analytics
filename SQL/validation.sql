-- =========================================================
-- ADMM Case Study - ShopX E-Commerce Analytics
-- Data Validation Queries
-- =========================================================

USE shopx_dw;


-- =========================================================
-- 1. Check total customers
-- =========================================================

SELECT COUNT(*) AS total_customers
FROM customers;


-- =========================================================
-- 2. Check total carriers
-- =========================================================

SELECT COUNT(DISTINCT carrier_id) AS total_carriers
FROM carriers;


-- =========================================================
-- 3. Check total orders
-- =========================================================

SELECT COUNT(*) AS total_orders
FROM orders;


-- =========================================================
-- 4. Check total order items
-- =========================================================

SELECT COUNT(*) AS total_order_items
FROM order_items;


-- =========================================================
-- 5. Check total shipments
-- =========================================================

SELECT COUNT(*) AS total_shipments
FROM shipments;


-- =========================================================
-- 6. Check total shipment items
-- =========================================================

SELECT COUNT(*) AS total_shipment_items
FROM shipment_items;


-- =========================================================
-- 7. Check total delivery analytics records
-- =========================================================

SELECT COUNT(*) AS total_delivery_records
FROM delivery_analytics;


-- =========================================================
-- 8. Check duplicate customers
-- =========================================================

SELECT customer_id, COUNT(*) AS duplicate_count
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;


-- =========================================================
-- 9. Check duplicate orders
-- =========================================================

SELECT order_id, COUNT(*) AS duplicate_count
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;


-- =========================================================
-- 10. Check duplicate carriers
-- =========================================================

SELECT carrier_id, COUNT(*) AS duplicate_count
FROM carriers
GROUP BY carrier_id
HAVING COUNT(*) > 1;


-- =========================================================
-- 11. Check duplicate order items
-- =========================================================

SELECT order_id, item_id, COUNT(*) AS duplicate_count
FROM order_items
GROUP BY order_id, item_id
HAVING COUNT(*) > 1;


-- =========================================================
-- 12. Check duplicate shipment items
-- =========================================================

SELECT shipment_id, item_id, COUNT(*) AS duplicate_count
FROM shipment_items
GROUP BY shipment_id, item_id
HAVING COUNT(*) > 1;


-- =========================================================
-- 13. Check NULL customer IDs
-- =========================================================

SELECT *
FROM customers
WHERE customer_id IS NULL;


-- =========================================================
-- 14. Check NULL order IDs
-- =========================================================

SELECT *
FROM orders
WHERE order_id IS NULL;


-- =========================================================
-- 15. Check NULL shipment IDs
-- =========================================================

SELECT *
FROM shipments
WHERE shipment_id IS NULL;


-- =========================================================
-- 16. Check invalid order quantities
-- =========================================================

SELECT *
FROM order_items
WHERE quantity <= 0;


-- =========================================================
-- 17. Check delivery delay
-- =========================================================

SELECT
    delivery_id,
    expected_delivery_date,
    actual_delivery_date,
    delivery_delay
FROM delivery_analytics
ORDER BY delivery_delay DESC;


-- =========================================================
-- 18. Calculate average delivery delay
-- =========================================================

SELECT
    ROUND(AVG(delivery_delay), 2) AS average_delivery_delay
FROM delivery_analytics;


-- =========================================================
-- 19. Calculate average order processing time
-- =========================================================

SELECT
    ROUND(AVG(order_processing_days), 2)
        AS average_order_processing_days
FROM shipments;


-- =========================================================
-- 20. Calculate late delivery rate
-- =========================================================

SELECT
    ROUND(
        SUM(CASE
            WHEN delivery_delay > 0 THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS late_delivery_rate
FROM delivery_analytics;


-- =========================================================
-- 21. Calculate on-time delivery rate
-- =========================================================

SELECT
    ROUND(
        SUM(CASE
            WHEN delivery_delay <= 0 THEN 1
            ELSE 0
        END) * 100.0 / COUNT(*),
        2
    ) AS on_time_delivery_rate
FROM delivery_analytics;


-- =========================================================
-- 22. Carrier performance
-- =========================================================

SELECT
    carrier,
    ROUND(AVG(order_processing_days), 2)
        AS average_processing_days
FROM shipments
GROUP BY carrier;


-- =========================================================
-- 23. Delivery delay by carrier
-- =========================================================

SELECT
    s.carrier,
    ROUND(AVG(d.delivery_delay), 2)
        AS average_delivery_delay
FROM shipments s
JOIN delivery_analytics d
    ON s.order_id = d.order_id
GROUP BY s.carrier
ORDER BY average_delivery_delay DESC;


-- =========================================================
-- 24. Check foreign key relationship - Orders
-- =========================================================

SELECT o.*
FROM orders o
LEFT JOIN customers c
    ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;


-- =========================================================
-- 25. Check foreign key relationship - Shipments
-- =========================================================

SELECT s.*
FROM shipments s
LEFT JOIN orders o
    ON s.order_id = o.order_id
WHERE o.order_id IS NULL;


-- =========================================================
-- 26. Check delivery date consistency
-- =========================================================

SELECT *
FROM delivery_analytics
WHERE actual_delivery_date IS NULL
   OR expected_delivery_date IS NULL;


-- =========================================================
-- 27. Check negative delivery delays
-- =========================================================

SELECT *
FROM delivery_analytics
WHERE delivery_delay < 0;