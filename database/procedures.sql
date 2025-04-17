-- Stored Procedure: PlaceOrder
DELIMITER //

CREATE PROCEDURE PlaceOrder (
    IN p_order_id INT,
    IN p_customer_id INT,
    IN p_product_id INT,
    IN p_quantity INT,
    IN p_unit_price DECIMAL(10,2)
)
BEGIN
    DECLARE v_total DECIMAL(10,2);

    INSERT INTO Orders (order_id, customer_id, order_date, total_amount)
    VALUES (p_order_id, p_customer_id, CURRENT_DATE, 0);

    INSERT INTO OrderDetails (order_detail_id, order_id, product_id, quantity, unit_price)
    VALUES (p_order_id, p_order_id, p_product_id, p_quantity, p_unit_price);

    UPDATE Products
    SET stock_quantity = stock_quantity - p_quantity
    WHERE product_id = p_product_id;

    INSERT INTO InventoryLogs (log_id, product_id, change_type, quantity_changed)
    VALUES (p_order_id, p_product_id, 'order', -p_quantity);

    SET v_total = p_quantity * p_unit_price;

    UPDATE Orders
    SET total_amount = v_total
    WHERE order_id = p_order_id;
END //

DELIMITER ;



-- Stored Procedure: ReplenishStock
DELIMITER //

CREATE PROCEDURE ReplenishStock (
    IN p_product_id INT,
    IN p_quantity INT
)
BEGIN
    UPDATE Products
    SET stock_quantity = stock_quantity + p_quantity
    WHERE product_id = p_product_id;

    INSERT INTO InventoryLogs (log_id, product_id, change_type, quantity_changed)
    VALUES ((SELECT COALESCE(MAX(log_id), 0) + 1 FROM InventoryLogs), p_product_id, 'replenishment', p_quantity);
END //

DELIMITER ;



-- Stored Procedure: CategorizeCustomers


DELIMITER //

CREATE PROCEDURE CategorizeCustomers()
BEGIN
    DELETE FROM CustomerTiers;

    INSERT INTO CustomerTiers (customer_id, total_spent, tier)
    SELECT c.customer_id,
           SUM(o.total_amount),
           CASE
               WHEN SUM(o.total_amount) >= 1000 THEN 'Gold'
               WHEN SUM(o.total_amount) >= 500 THEN 'Silver'
               ELSE 'Bronze'
           END
    FROM Customers c
    JOIN Orders o ON c.customer_id = o.customer_id
    GROUP BY c.customer_id;
END //

DELIMITER ;
