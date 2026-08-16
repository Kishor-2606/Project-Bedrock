import logging
from datetime import date
from typing import Optional

from sqlalchemy import func, asc, desc
from sqlalchemy.orm import Session

from models import Expense, Category, User
from schemas import ExpenseCreate, ExpenseUpdate

logger = logging.getLogger(__name__)

sort_fields = {
    "amount": Expense.amount,
    "-amount": Expense.amount,
    "date": Expense.expense_date,
    "-date": Expense.expense_date,
    "title": Expense.title,
    "-title": Expense.title,
}


def _expense_to_dict(expense):
    return {
        "id": expense.id,
        "title": expense.title,
        "amount": float(expense.amount),
        "category": expense.category.category_name if expense.category else "Unknown",
        "description": expense.description,
        "expense_date": expense.expense_date,
        "created_at": expense.created_at,
        "is_recurring": expense.is_recurring,
        "user_id": expense.user_id,
    }


def _get_or_create_category(db, category_name):
    normalized = category_name.strip().title()

    category = (
        db.query(Category)
        .filter(func.lower(Category.category_name) == normalized.lower())
        .first()
    )

    if not category:
        logger.info("Category '%s' not found — creating it.", normalized)
        category = Category(category_name=normalized)
        db.add(category)
        db.flush()

    return category


def create_expense(db, data):
    category = _get_or_create_category(db, data.category)

    new_expense = Expense(
        user_id=data.user_id if data.user_id else 1,
        category_id=category.category_id,
        title=data.title,
        amount=data.amount,
        description=data.description,
        expense_date=data.expense_date if data.expense_date else date.today(),
        is_recurring=data.is_recurring if data.is_recurring is not None else False,
    )

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    logger.info("Created expense: id=%d title='%s' amount=%.2f", new_expense.id, new_expense.title, new_expense.amount)
    return _expense_to_dict(new_expense)


def get_all_expenses(db, category=None, min_amount=None, max_amount=None, sort=None, skip=0, limit=10):
    query = db.query(Expense).join(Expense.category)

    if category:
        query = query.filter(func.lower(Category.category_name) == category.strip().lower())

    if min_amount is not None:
        query = query.filter(Expense.amount >= min_amount)

    if max_amount is not None:
        query = query.filter(Expense.amount <= max_amount)

    if sort and sort in sort_fields:
        col = sort_fields[sort]
        if sort.startswith("-"):
            query = query.order_by(desc(col))
        else:
            query = query.order_by(asc(col))
    else:
        query = query.order_by(desc(Expense.created_at))

    expenses = query.offset(skip).limit(limit).all()
    return [_expense_to_dict(e) for e in expenses]


def get_expense_by_id(db, expense_id):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense is None:
        logger.warning("Expense id=%d not found.", expense_id)
        return None

    return _expense_to_dict(expense)


def update_expense(db, expense_id, data):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense is None:
        logger.warning("Update failed — expense id=%d not found.", expense_id)
        return None

    if data.title is not None:
        expense.title = data.title

    if data.amount is not None:
        expense.amount = data.amount

    if data.category is not None:
        category = _get_or_create_category(db, data.category)
        expense.category_id = category.category_id

    if data.description is not None:
        expense.description = data.description

    if data.expense_date is not None:
        expense.expense_date = data.expense_date

    if data.is_recurring is not None:
        expense.is_recurring = data.is_recurring

    try:
        db.commit()
        db.refresh(expense)
    except Exception:
        db.rollback()
        logger.error("Failed to update expense id=%d — rolled back.", expense_id)
        raise

    logger.info("Updated expense: id=%d", expense.id)
    return _expense_to_dict(expense)


def delete_expense(db, expense_id):
    expense = db.query(Expense).filter(Expense.id == expense_id).first()

    if expense is None:
        logger.warning("Delete failed — expense id=%d not found.", expense_id)
        return False

    db.delete(expense)
    db.commit()

    logger.info("Deleted expense: id=%d", expense_id)
    return True


def get_total(db):
    result = db.query(
        func.sum(Expense.amount).label("total"),
        func.count(Expense.id).label("count"),
    ).first()

    return {
        "total": float(result.total) if result.total else 0.0,
        "count": result.count if result.count else 0,
    }


def get_highest_expense(db):
    expense = db.query(Expense).order_by(desc(Expense.amount)).first()

    if expense is None:
        return None

    return _expense_to_dict(expense)
