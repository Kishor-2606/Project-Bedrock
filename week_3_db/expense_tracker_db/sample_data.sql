USE expense_tracker_db;

-- Users
INSERT INTO users (username, email) VALUES
('igris', 'igris@example.com'),
('sasmitha', 'sasmitha@example.com');

-- Categories
INSERT INTO categories (category_name) VALUES
('Food'),
('Transport'),
('Subscriptions'),
('Electronics');

-- Expenses
INSERT INTO expenses
(user_id, category_id, title, price, expense_date)
VALUES
(1, 1, 'Groceries',    1200.00, '2026-08-01'),
(1, 1, 'Restaurant',    650.00, '2026-08-03'),
(1, 2, 'Bus Pass',      400.00, '2026-08-01'),
(1, 3, 'ChatGPT Plus', 1650.00, '2026-08-05'),
(1, 4, 'ESP32 Board',   450.00, '2026-08-06'),
(2, 1, 'Groceries',     900.00, '2026-08-02'),
(2, 3, 'Netflix',       499.00, '2026-08-04');
