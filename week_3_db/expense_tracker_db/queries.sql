USE expense_tracker_db;

-- ============================================================
-- 1. BASIC READ
-- ============================================================

SELECT * FROM users;
SELECT * FROM categories;
SELECT * FROM expenses;

-- ============================================================
-- 2. CRUD
-- ============================================================

-- CREATE
INSERT INTO expenses
(user_id, category_id, title, price, expense_date)
VALUES (1, 2, 'Auto Fare', 180.00, '2026-08-07');

-- READ
SELECT *
FROM expenses
WHERE user_id = 1;

-- UPDATE
UPDATE expenses
SET price = 500.00
WHERE title = 'Restaurant';

-- DELETE
DELETE FROM expenses
WHERE title = 'Auto Fare';

-- ============================================================
-- 3. DISTINCT / ORDER BY / LIMIT
-- ============================================================

SELECT DISTINCT category_id
FROM expenses;

SELECT title, price
FROM expenses
ORDER BY price DESC
LIMIT 3;

-- ============================================================
-- 4. FILTERING
-- ============================================================

SELECT *
FROM expenses
WHERE user_id = 1 AND price > 500;

SELECT *
FROM expenses
WHERE category_id = 1 OR category_id = 3;

SELECT *
FROM expenses
WHERE NOT category_id = 1;

SELECT *
FROM expenses
WHERE category_id IN (1, 3);

SELECT *
FROM expenses
WHERE price BETWEEN 400 AND 1000;

SELECT *
FROM expenses
WHERE title LIKE '%Groc%';

SELECT *
FROM expenses
WHERE notes IS NULL;

SELECT *
FROM expenses
WHERE notes IS NOT NULL;

-- ============================================================
-- 5. AGGREGATE FUNCTIONS
-- ============================================================

SELECT COUNT(*) AS total_expenses
FROM expenses
WHERE user_id = 1;

SELECT SUM(price) AS total_spent
FROM expenses
WHERE user_id = 1;

SELECT AVG(price) AS avg_spent
FROM expenses
WHERE user_id = 1;

SELECT MIN(price) AS cheapest,
       MAX(price) AS costliest
FROM expenses;

-- ============================================================
-- 6. STRING FUNCTIONS
-- ============================================================

SELECT UPPER(title) AS title_upper
FROM expenses;

SELECT LOWER(title) AS title_lower
FROM expenses;

SELECT title,
       LENGTH(title) AS title_length
FROM expenses;

SELECT CONCAT(title, ' - Rs.', price) AS summary_line
FROM expenses;

-- ============================================================
-- 7. DATE FUNCTIONS
-- ============================================================

SELECT NOW() AS current_datetime;

SELECT CURDATE() AS today;

SELECT title,
       YEAR(expense_date) AS yr,
       MONTH(expense_date) AS mo,
       DAY(expense_date) AS dy
FROM expenses;

-- ============================================================
-- 8. GROUP BY / HAVING
-- ============================================================

-- Total spend per category
SELECT c.category_name,
       SUM(e.price) AS total_spent
FROM expenses e
JOIN categories c
    ON e.category_id = c.category_id
GROUP BY c.category_id, c.category_name
ORDER BY total_spent DESC;

-- Categories where spending crossed 1000
SELECT c.category_name,
       SUM(e.price) AS total_spent
FROM expenses e
JOIN categories c
    ON e.category_id = c.category_id
GROUP BY c.category_id, c.category_name
HAVING SUM(e.price) > 1000;

-- Average expense per user
SELECT u.username,
       AVG(e.price) AS avg_expense
FROM expenses e
JOIN users u
    ON e.user_id = u.user_id
GROUP BY u.user_id, u.username;

-- ============================================================
-- 9. INNER JOIN
-- ============================================================

SELECT e.title,
       e.price,
       u.username,
       c.category_name
FROM expenses e
INNER JOIN users u
    ON e.user_id = u.user_id
INNER JOIN categories c
    ON e.category_id = c.category_id
ORDER BY e.expense_date;

-- ============================================================
-- 10. LEFT JOIN
-- ============================================================

SELECT c.category_name,
       e.title,
       e.price
FROM categories c
LEFT JOIN expenses e
    ON c.category_id = e.category_id;

-- ============================================================
-- 11. RIGHT JOIN
-- ============================================================

SELECT u.username,
       e.title
FROM expenses e
RIGHT JOIN users u
    ON e.user_id = u.user_id;

-- ============================================================
-- 12. FULL OUTER JOIN SIMULATION IN MYSQL
-- ============================================================

SELECT c.category_name,
       e.title
FROM categories c
LEFT JOIN expenses e
    ON c.category_id = e.category_id

UNION

SELECT c.category_name,
       e.title
FROM categories c
RIGHT JOIN expenses e
    ON c.category_id = e.category_id;

-- ============================================================
-- 13. SELF JOIN
-- ============================================================

SELECT a.title AS expense_1,
       b.title AS expense_2,
       a.category_id
FROM expenses a
JOIN expenses b
    ON a.category_id = b.category_id
   AND a.expense_id < b.expense_id;

-- ============================================================
-- 14. CROSS JOIN
-- ============================================================

SELECT u.username,
       c.category_name
FROM users u
CROSS JOIN categories c;

-- ============================================================
-- 15. PRACTICAL EXPENSE REPORTS
-- ============================================================

-- Highest expense
SELECT title, price
FROM expenses
ORDER BY price DESC
LIMIT 1;

-- Total spending per user
SELECT u.username,
       SUM(e.price) AS total_spent
FROM users u
JOIN expenses e
    ON u.user_id = e.user_id
GROUP BY u.user_id, u.username
ORDER BY total_spent DESC;

-- User + category spending
SELECT u.username,
       c.category_name,
       SUM(e.price) AS total_spent
FROM users u
JOIN expenses e
    ON u.user_id = e.user_id
JOIN categories c
    ON e.category_id = c.category_id
GROUP BY u.user_id, u.username,
         c.category_id, c.category_name
ORDER BY u.username, total_spent DESC;

-- Categories with more than one expense
SELECT c.category_name,
       COUNT(e.expense_id) AS expense_count
FROM categories c
LEFT JOIN expenses e
    ON c.category_id = e.category_id
GROUP BY c.category_id, c.category_name
HAVING COUNT(e.expense_id) > 1;

-- Expenses above the overall average
SELECT title, price
FROM expenses
WHERE price > (
    SELECT AVG(price)
    FROM expenses
)
ORDER BY price DESC;

-- Monthly spending
SELECT YEAR(expense_date) AS expense_year,
       MONTH(expense_date) AS expense_month,
       SUM(price) AS total_spent
FROM expenses
GROUP BY YEAR(expense_date), MONTH(expense_date)
ORDER BY expense_year, expense_month;
