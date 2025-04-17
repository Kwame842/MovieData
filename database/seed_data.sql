--INSERTION INTO PRODUCTS

INSERT INTO Products (product_id, name, category, price, stock_quantity, reorder_level) VALUES
(1, 'Laptop', 'Electronics', 800.00, 10, 5),
(2, 'Smartphone', 'Electronics', 500.00, 3, 5),
(3, 'Office Chair', 'Furniture', 150.00, 20, 10),
(4, 'Desk Lamp', 'Lighting', 40.00, 2, 5),
(5, 'Notebook', 'Stationery', 5.00, 100, 50),
(6, 'Pen', 'Stationery', 1.50, 200, 100),
(7, 'Monitor', 'Electronics', 200.00, 4, 5),
(8, 'Keyboard', 'Electronics', 50.00, 8, 3),
(9, 'Mouse', 'Electronics', 25.00, 6, 5),
(10, 'Backpack', 'Accessories', 60.00, 12, 6);


-- INSERTION INTO Customers

INSERT INTO Customers (customer_id, name, email, phone) VALUES
(1, 'Alice Johnson', 'alice@example.com', '555-1234'),
(2, 'Bob Smith', 'bob@example.com', '555-5678'),
(3, 'Carol Lee', 'carol@example.com', '555-9012'),
(4, 'David Wright', 'david@example.com', '555-3456'),
(5, 'Eva Adams', 'eva@example.com', '555-7890'),
(6, 'Frank Mills', 'frank@example.com', '555-4321'),
(7, 'Grace Young', 'grace@example.com', '555-6789'),
(8, 'Henry Thomas', 'henry@example.com', '555-8765'),
(9, 'Ivy Nelson', 'ivy@example.com', '555-2345'),
(10, 'Jack Davis', 'jack@example.com', '555-1111');


--INSERTION INTO Orders

INSERT INTO Orders (order_id, customer_id, order_date, total_amount) VALUES
(101, 1, '2025-04-10', 850.00),
(102, 2, '2025-04-11', 1150.00),
(103, 3, '2025-04-12', 120.00),
(104, 4, '2025-04-12', 225.00),
(105, 5, '2025-04-13', 75.00),
(106, 6, '2025-04-13', 610.00),
(107, 7, '2025-04-14', 850.00),
(108, 8, '2025-04-14', 350.00),
(109, 9, '2025-04-15', 425.00),
(110, 10, '2025-04-15', 95.00);


-- INSERTION INTO OrderDetails

INSERT INTO OrderDetails (order_detail_id, order_id, product_id, quantity, unit_price) VALUES
(101, 101, 1, 1, 800.00),
(102, 101, 5, 10, 5.00),
(103, 102, 2, 2, 500.00),
(104, 102, 3, 1, 150.00),
(105, 103, 4, 3, 40.00),
(106, 104, 6, 50, 1.50),
(107, 105, 5, 15, 5.00),
(108, 106, 7, 3, 200.00),
(109, 106, 9, 2, 25.00),
(110, 107, 1, 1, 800.00),
(111, 107, 6, 20, 1.50),
(112, 108, 8, 7, 50.00),
(113, 109, 10, 5, 60.00),
(114, 109, 3, 1, 150.00),
(115, 110, 5, 5, 5.00),
(116, 110, 9, 1, 25.00);



-- INSERTION INTO InventoryLogs

INSERT INTO InventoryLogs (log_id, product_id, change_date, change_type, quantity_changed) VALUES
(1, 1, NOW(), 'order', -1),
(2, 5, NOW(), 'order', -10),
(3, 2, NOW(), 'order', -2),
(4, 3, NOW(), 'order', -2),
(5, 4, NOW(), 'order', -3),
(6, 6, NOW(), 'order', -70),
(7, 7, NOW(), 'order', -3),
(8, 9, NOW(), 'order', -3),
(9, 8, NOW(), 'order', -7),
(10, 10, NOW(), 'order', -5);
