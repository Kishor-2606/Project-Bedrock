#Expense Tracker API - Week 4

from sqlalchemy import (
    Column,
    Integer,
    String,
    DECIMAL,
    Date,
    DateTime,
    Boolean,
    ForeignKey,
    func,
)
from sqlalchemy.orm import relationship
from database import Base


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, server_default=func.now())

    expenses = relationship("Expense", back_populates="user")


class Category(Base):
    __tablename__ = "categories"

    category_id = Column(Integer, primary_key=True, autoincrement=True)
    category_name = Column(String(30), nullable=False, unique=True)

    expenses = relationship("Expense", back_populates="category")


class Expense(Base):
    __tablename__ = "expenses"

    id = Column("expense_id", Integer, primary_key=True, autoincrement=True)

    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.category_id", ondelete="RESTRICT"), nullable=False)

    title = Column(String(50), nullable=False)
    amount = Column("price", DECIMAL(10, 2), nullable=False)
    description = Column("notes", String(255), nullable=True)
    expense_date = Column(Date, nullable=False)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    is_recurring = Column(Boolean, nullable=False, default=False)

    user = relationship("User", back_populates="expenses")
    category = relationship("Category", back_populates="expenses")

    def __repr__(self):
        return f"<Expense id={self.id} title='{self.title}' amount={self.amount}>"
