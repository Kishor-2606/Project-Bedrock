-- ============================================================
-- PROJECT BEDROCK - WEEK 3
-- Schema: expense_tracker_db
-- Goal: back the existing Expense Tracker FastAPI project
-- with a real relational schema instead of an in-memory list.
-- ============================================================

DROP DATABASE IF EXISTS expense_tracker_db;
CREATE DATABASE expense_tracker_db;
USE expense_tracker_db;

CREATE TABLE users (
    user_id     INT AUTO_INCREMENT PRIMARY KEY,
    username    VARCHAR(50)  NOT NULL,
    email       VARCHAR(100) NOT NULL UNIQUE,
    created_at  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE categories (
    category_id     INT AUTO_INCREMENT PRIMARY KEY,
    category_name   VARCHAR(30) NOT NULL UNIQUE
);

CREATE TABLE expenses (
    expense_id   INT AUTO_INCREMENT PRIMARY KEY,
    user_id      INT NOT NULL,
    category_id  INT NOT NULL,
    title        VARCHAR(50)  NOT NULL,
    price        DECIMAL(10,2) NOT NULL,
    notes        VARCHAR(255) NULL,
    expense_date DATE NOT NULL DEFAULT (CURRENT_DATE),
    created_at   DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_expenses_user
        FOREIGN KEY (user_id) REFERENCES users(user_id)
        ON DELETE CASCADE,

    CONSTRAINT fk_expenses_category
        FOREIGN KEY (category_id) REFERENCES categories(category_id)
        ON DELETE RESTRICT,

    CONSTRAINT chk_price_positive CHECK (price > 0)
);

ALTER TABLE expenses ADD COLUMN is_recurring BOOLEAN NOT NULL DEFAULT FALSE;

CREATE INDEX idx_expenses_category ON expenses(category_id);
CREATE INDEX idx_expenses_date ON expenses(expense_date);
