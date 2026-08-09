USE report_card_db;

-- Classes
INSERT INTO classes (class_name) VALUES
('10-A'),
('10-B');

-- Students
INSERT INTO students (student_name, class_id, dob, email) VALUES
('Sasmitha S S', 1, '2009-03-14', 'sasmitha.student@example.com'),
('Arun Kumar',   1, '2009-06-21', 'arun.student@example.com'),
('Divya R',      2, '2009-01-09', 'divya.student@example.com');

-- Subjects
INSERT INTO subjects (subject_name) VALUES
('Maths'),
('Science'),
('English'),
('Social Science');

-- Marks
INSERT INTO marks (student_id, subject_id, marks_obtained, exam_date) VALUES
(1, 1, 92, '2026-08-01'),
(1, 2, 88, '2026-08-01'),
(1, 3, 76, '2026-08-01'),
(1, 4, 81, '2026-08-01'),
(2, 1, 65, '2026-08-01'),
(2, 2, 70, '2026-08-01'),
(2, 3, 58, '2026-08-01'),
(3, 1, 45, '2026-08-01'),
(3, 2, 52, '2026-08-01');
