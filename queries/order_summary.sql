-- Order Summary
SELECT o.order_id, c.name AS customer_name, o.order_date, o.total_amount,
       SUM(od.quantity) AS total_items
FROM Orders o
JOIN Customers c ON o.customer_id = c.customer_id
JOIN OrderDetails od ON o.order_id = od.order_id
GROUP BY o.order_id, c.name, o.order_date, o.total_amount;
