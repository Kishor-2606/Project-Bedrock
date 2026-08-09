-- ============================================================
-- PROJECT BEDROCK - WEEK 3
-- Schema: report_card_db
-- Goal: back the existing Student Report Card FastAPI project
-- with a real relational schema instead of an in-memory dict.
-- ============================================================

DROP DATABASE IF EXISTS report_card_db;
CREATE DATABASE report_card_db;
USE report_card_db;

CREATE TABLE classes (
    class_id     INT AUTO_INCREMENT PRIMARY KEY,
    class_name   VARCHAR(20) NOT NULL UNIQUE
);

CREATE TABLE students (
    student_id      INT AUTO_INCREMENT PRIMARY KEY,
    student_name    VARCHAR(50)  NOT NULL,
    class_id        INT NOT NULL,
    dob             DATE NULL,
    email           VARCHAR(100) NULL UNIQUE,
    enrolled_date   DATE NOT NULL DEFAULT (CURRENT_DATE),

    CONSTRAINT fk_students_class
        FOREIGN KEY (class_id) REFERENCES classes(class_id)
        ON DELETE RESTRICT
);

CREATE TABLE subjects (
    subject_id    INT AUTO_INCREMENT PRIMARY KEY,
    subject_name  VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE marks (
    mark_id         INT AUTO_INCREMENT PRIMARY KEY,
    student_id      INT NOT NULL,
    subject_id      INT NOT NULL,
    marks_obtained  INT NOT NULL,
    exam_date       DATE NOT NULL DEFAULT (CURRENT_DATE),

    CONSTRAINT fk_marks_student
        FOREIGN KEY (student_id) REFERENCES students(student_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_marks_subject
        FOREIGN KEY (subject_id) REFERENCES subjects(subject_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_marks_range CHECK (marks_obtained BETWEEN 0 AND 100),

    CONSTRAINT uq_student_subject UNIQUE (student_id, subject_id)
);

ALTER TABLE students ADD COLUMN is_active BOOLEAN NOT NULL DEFAULT TRUE;

CREATE INDEX idx_marks_student ON marks(student_id);
CREATE INDEX idx_students_class ON students(class_id);
