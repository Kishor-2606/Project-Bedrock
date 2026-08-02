from fastapi import FastAPI, HTTPException, status

from tracker import ExpenseTracker
from schemas import (
    ExpenseRequest,
    ExpenseResponse,
    ExpenseUpdate,
    TotalResponse
)

app = FastAPI(title="Expense Tracker API")

tracker = ExpenseTracker()


@app.get("/")
def home():
    return {"message": "Expense Tracker API"}


@app.post(
    "/expenses",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED
)
def create_expense(expense: ExpenseRequest):

    new_expense = tracker.add_expense(
        expense.title,
        expense.price,
        expense.category
    )

    return {
        "id": new_expense.id,
        "title": new_expense.title,
        "price": new_expense.price,
        "category": new_expense.category
    }


@app.get(
    "/expenses",
    response_model=list[ExpenseResponse]
)
def view_expenses():

    result = []

    for expense in tracker.get_all_expenses():

        result.append({
            "id": expense.id,
            "title": expense.title,
            "price": expense.price,
            "category": expense.category
        })

    return result


@app.get(
    "/expenses/{expense_id}",
    response_model=ExpenseResponse
)
def get_expense(expense_id: int):

    expense = tracker.get_expense(expense_id)

    if expense is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "id": expense.id,
        "title": expense.title,
        "price": expense.price,
        "category": expense.category
    }

@app.patch(
    "/expenses/{expense_id}",
    response_model=ExpenseResponse
)
def update_expense(
    expense_id: int,
    expense: ExpenseUpdate
):

    updated = tracker.update_expense(
        expense_id,
        expense.title,
        expense.price,
        expense.category
    )

    if updated is None:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )

    return {
        "id": updated.id,
        "title": updated.title,
        "price": updated.price,
        "category": updated.category
    }

@app.delete(
    "/expenses/{expense_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_expense(expense_id: int):

    deleted = tracker.delete_expense(expense_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Expense not found"
        )


@app.get(
    "/expenses/total",
    response_model=TotalResponse
)
def show_total():

    return {
        "total": tracker.calculate_total()
    }


@app.get(
    "/expenses/filter/title/{title}",
    response_model=list[ExpenseResponse]
)
def filter_title(title: str):

    expenses = tracker.filter_by_title(title)

    return [
        {
            "id": e.id,
            "title": e.title,
            "price": e.price,
            "category": e.category
        }
        for e in expenses
    ]


@app.get(
    "/expenses/filter/category/{category}",
    response_model=list[ExpenseResponse]
)
def filter_category(category: str):

    expenses = tracker.filter_by_category(category)

    return [
        {
            "id": e.id,
            "title": e.title,
            "price": e.price,
            "category": e.category
        }
        for e in expenses
    ]


@app.get(
    "/expenses/filter/price",
    response_model=list[ExpenseResponse]
)
def filter_price(
    min_price: float,
    max_price: float
):

    expenses = tracker.filter_by_price(
        min_price,
        max_price
    )

    return [
        {
            "id": e.id,
            "title": e.title,
            "price": e.price,
            "category": e.category
        }
        for e in expenses
    ]