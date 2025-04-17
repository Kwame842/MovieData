-- Low Stock Report
SELECT product_id, name, stock_quantity, reorder_level
FROM Products
WHERE stock_quantity < reorder_level;
