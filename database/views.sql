-- View: Order Summary
CREATE VIEW OrderSummaryView AS
SELECT o.order_id, c.name AS customer_name, o.order_date, o.total_amount,
       COUNT(od.order_detail_id) AS item_count
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN OrderDetails od ON o.order_id = od.order_id
GROUP BY o.order_id, c.name, o.order_date, o.total_amount;

-- View: Low Stock
CREATE VIEW LowStockView AS
SELECT product_id, name, stock_quantity, reorder_level
FROM Products
WHERE stock_quantity < reorder_level;
