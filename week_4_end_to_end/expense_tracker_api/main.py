#Expense Tracker API - Week 4

import logging
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, Query, status
from sqlalchemy.orm import Session

import service
from database import Base, engine, get_db
from schemas import ExpenseCreate, ExpenseResponse, ExpenseUpdate, TotalResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables verified / created successfully.")
    except Exception as exc:
        logger.warning("Could not verify database tables: %s", exc)
    yield


app = FastAPI(
    title="Expense Tracker API — Week 4",
    description="End-to-End Expense Tracker — Week 4 of Project Bedrock.",
    version="4.0.0",
    lifespan=lifespan,
)


@app.get("/", tags=["Health"])
def root():
    return {"message": "Expense Tracker API — Week 4", "status": "running"}


@app.post("/expenses", response_model=ExpenseResponse, status_code=status.HTTP_201_CREATED, tags=["Expenses"])
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    return service.create_expense(db, expense)


@app.get("/expenses", response_model=list[ExpenseResponse], tags=["Expenses"])
def get_expenses(
    category: Optional[str] = Query(default=None),
    min_amount: Optional[float] = Query(default=None, ge=0),
    max_amount: Optional[float] = Query(default=None, ge=0),
    sort: Optional[str] = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return service.get_all_expenses(
        db,
        category=category,
        min_amount=min_amount,
        max_amount=max_amount,
        sort=sort,
        skip=skip,
        limit=limit,
    )


@app.get("/expenses/total", response_model=TotalResponse, tags=["Analytics"])
def get_total(db: Session = Depends(get_db)):
    return service.get_total(db)


@app.get("/expenses/highest", response_model=ExpenseResponse, tags=["Analytics"])
def get_highest(db: Session = Depends(get_db)):
    result = service.get_highest_expense(db)
    if result is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No expenses found.")
    return result


@app.get("/expenses/{expense_id}", response_model=ExpenseResponse, tags=["Expenses"])
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    expense = service.get_expense_by_id(db, expense_id)
    if expense is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense with id {expense_id} not found.")
    return expense


@app.patch("/expenses/{expense_id}", response_model=ExpenseResponse, tags=["Expenses"])
def update_expense(expense_id: int, expense: ExpenseUpdate, db: Session = Depends(get_db)):
    updated = service.update_expense(db, expense_id, expense)
    if updated is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense with id {expense_id} not found.")
    return updated


@app.delete("/expenses/{expense_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Expenses"])
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    deleted = service.delete_expense(db, expense_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Expense with id {expense_id} not found.")
