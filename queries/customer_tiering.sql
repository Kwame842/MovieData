-- Customer Tiering
SELECT c.customer_id, c.name, SUM(o.total_amount) AS total_spent,
       CASE
           WHEN SUM(o.total_amount) >= 1000 THEN 'Gold'
           WHEN SUM(o.total_amount) >= 500 THEN 'Silver'
           ELSE 'Bronze'
       END AS customer_tier
FROM Customers c
JOIN Orders o ON c.customer_id = o.customer_id
GROUP BY c.customer_id, c.name;
