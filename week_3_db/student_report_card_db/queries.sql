USE report_card_db;

-- ============================================================
-- 1. BASIC READ
-- ============================================================

SELECT * FROM classes;
SELECT * FROM students;
SELECT * FROM subjects;
SELECT * FROM marks;

-- ============================================================
-- 2. CRUD
-- ============================================================

-- CREATE
INSERT INTO marks (student_id, subject_id, marks_obtained)
VALUES (3, 3, 60);

-- READ
SELECT *
FROM marks
WHERE student_id = 1;

-- UPDATE
UPDATE marks
SET marks_obtained = 95
WHERE student_id = 1 AND subject_id = 1;

-- DELETE
DELETE FROM marks
WHERE student_id = 3 AND subject_id = 3;

-- ============================================================
-- 3. FILTERING
-- ============================================================

SELECT *
FROM marks
WHERE subject_id = 1 AND marks_obtained >= 90;

SELECT *
FROM marks
WHERE subject_id = 1 OR subject_id = 2;

SELECT *
FROM marks
WHERE NOT subject_id = 1;

SELECT *
FROM students
WHERE class_id IN (1, 2);

SELECT *
FROM marks
WHERE marks_obtained BETWEEN 50 AND 89;

SELECT *
FROM students
WHERE student_name LIKE 'S%';

SELECT *
FROM students
WHERE dob IS NULL;

SELECT *
FROM students
WHERE dob IS NOT NULL;

-- ============================================================
-- 4. DISTINCT / ORDER BY / LIMIT
-- ============================================================

SELECT DISTINCT class_id
FROM students;

SELECT student_id, subject_id, marks_obtained
FROM marks
ORDER BY marks_obtained DESC
LIMIT 2;

-- ============================================================
-- 5. AGGREGATE FUNCTIONS
-- ============================================================

SELECT COUNT(*) AS subjects_taken
FROM marks
WHERE student_id = 1;

SELECT SUM(marks_obtained) AS total_marks
FROM marks
WHERE student_id = 1;

SELECT AVG(marks_obtained) AS average_marks
FROM marks
WHERE student_id = 1;

SELECT MIN(marks_obtained) AS lowest,
       MAX(marks_obtained) AS highest
FROM marks;

-- ============================================================
-- 6. STRING FUNCTIONS
-- ============================================================

SELECT UPPER(student_name) AS name_upper
FROM students;

SELECT LOWER(student_name) AS name_lower
FROM students;

SELECT student_name,
       LENGTH(student_name) AS name_length
FROM students;

SELECT CONCAT(student_name, ' (', class_id, ')') AS display_name
FROM students;

-- ============================================================
-- 7. DATE FUNCTIONS
-- ============================================================

SELECT NOW() AS current_datetime;

SELECT CURDATE() AS today;

SELECT student_name,
       YEAR(dob) AS birth_year,
       MONTH(dob) AS birth_month
FROM students;

-- ============================================================
-- 8. GROUP BY / HAVING
-- ============================================================

-- Average marks per student
SELECT s.student_name,
       ROUND(AVG(m.marks_obtained), 2) AS average_marks
FROM marks m
JOIN students s
    ON m.student_id = s.student_id
GROUP BY s.student_id, s.student_name;

-- Average marks class-wise
SELECT c.class_name,
       ROUND(AVG(m.marks_obtained), 2) AS class_average
FROM marks m
JOIN students s
    ON m.student_id = s.student_id
JOIN classes c
    ON s.class_id = c.class_id
GROUP BY c.class_id, c.class_name;

-- Students whose average is above 80
SELECT s.student_name,
       ROUND(AVG(m.marks_obtained), 2) AS average_marks
FROM marks m
JOIN students s
    ON m.student_id = s.student_id
GROUP BY s.student_id, s.student_name
HAVING AVG(m.marks_obtained) > 80;

-- Student count per class
SELECT c.class_name,
       COUNT(s.student_id) AS student_count
FROM classes c
LEFT JOIN students s
    ON s.class_id = c.class_id
GROUP BY c.class_id, c.class_name;

-- ============================================================
-- 9. INNER JOIN
-- ============================================================

SELECT s.student_name,
       sub.subject_name,
       m.marks_obtained
FROM marks m
INNER JOIN students s
    ON m.student_id = s.student_id
INNER JOIN subjects sub
    ON m.subject_id = sub.subject_id
ORDER BY s.student_name, sub.subject_name;

-- ============================================================
-- 10. LEFT JOIN
-- ============================================================

SELECT s.student_name,
       m.marks_obtained
FROM students s
LEFT JOIN marks m
    ON s.student_id = m.student_id;

-- ============================================================
-- 11. RIGHT JOIN
-- ============================================================

SELECT s.student_name,
       m.marks_obtained
FROM marks m
RIGHT JOIN students s
    ON m.student_id = s.student_id;

-- ============================================================
-- 12. FULL OUTER JOIN SIMULATION IN MYSQL
-- ============================================================

SELECT s.student_name,
       sub.subject_name
FROM students s
LEFT JOIN marks m
    ON s.student_id = m.student_id
LEFT JOIN subjects sub
    ON m.subject_id = sub.subject_id

UNION

SELECT s.student_name,
       sub.subject_name
FROM subjects sub
LEFT JOIN marks m
    ON sub.subject_id = m.subject_id
LEFT JOIN students s
    ON m.student_id = s.student_id;

-- ============================================================
-- 13. SELF JOIN
-- ============================================================

SELECT a.student_name AS student_1,
       b.student_name AS student_2,
       a.class_id
FROM students a
JOIN students b
    ON a.class_id = b.class_id
   AND a.student_id < b.student_id;

-- ============================================================
-- 14. CROSS JOIN
-- ============================================================

SELECT s.student_name,
       sub.subject_name
FROM students s
CROSS JOIN subjects sub;

-- ============================================================
-- 15. REPORT-CARD STYLE QUERIES
-- ============================================================

-- Complete report for every student
SELECT s.student_name,
       c.class_name,
       sub.subject_name,
       m.marks_obtained,
       m.exam_date
FROM students s
JOIN classes c
    ON s.class_id = c.class_id
JOIN marks m
    ON s.student_id = m.student_id
JOIN subjects sub
    ON m.subject_id = sub.subject_id
ORDER BY s.student_name, sub.subject_id;

-- Highest-scoring student by average
SELECT s.student_name,
       ROUND(AVG(m.marks_obtained), 2) AS average_marks
FROM students s
JOIN marks m
    ON s.student_id = m.student_id
GROUP BY s.student_id, s.student_name
ORDER BY average_marks DESC
LIMIT 1;

-- Subject-wise average
SELECT sub.subject_name,
       ROUND(AVG(m.marks_obtained), 2) AS subject_average
FROM subjects sub
JOIN marks m
    ON sub.subject_id = m.subject_id
GROUP BY sub.subject_id, sub.subject_name
ORDER BY subject_average DESC;

-- Students who scored 90 or above in any subject
SELECT DISTINCT s.student_name
FROM students s
JOIN marks m
    ON s.student_id = m.student_id
WHERE m.marks_obtained >= 90;

-- Students with total marks above 250
SELECT s.student_name,
       SUM(m.marks_obtained) AS total_marks
FROM students s
JOIN marks m
    ON s.student_id = m.student_id
GROUP BY s.student_id, s.student_name
HAVING SUM(m.marks_obtained) > 250
ORDER BY total_marks DESC;
