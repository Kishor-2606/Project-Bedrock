from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class ExpenseCreate(BaseModel):
    title: str = Field(min_length=2, max_length=50)
    amount: float = Field(gt=0)
    category: str = Field(min_length=2, max_length=30)
    description: Optional[str] = Field(default=None, max_length=255)
    expense_date: Optional[date] = Field(default=None)
    user_id: Optional[int] = Field(default=1, ge=1)
    is_recurring: Optional[bool] = Field(default=False)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("title must not be blank or whitespace only")
        return v.strip()

    @field_validator("category")
    @classmethod
    def category_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("category must not be blank or whitespace only")
        return v.strip()


class ExpenseUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=2, max_length=50)
    amount: Optional[float] = Field(default=None, gt=0)
    category: Optional[str] = Field(default=None, min_length=2, max_length=30)
    description: Optional[str] = Field(default=None, max_length=255)
    expense_date: Optional[date] = Field(default=None)
    is_recurring: Optional[bool] = Field(default=None)

    @field_validator("title")
    @classmethod
    def title_must_not_be_blank(cls, v):
        if v is not None and not v.strip():
            raise ValueError("title must not be blank or whitespace only")
        return v.strip() if v else v

    @field_validator("category")
    @classmethod
    def category_must_not_be_blank(cls, v):
        if v is not None and not v.strip():
            raise ValueError("category must not be blank or whitespace only")
        return v.strip() if v else v


class ExpenseResponse(BaseModel):
    id: int
    title: str
    amount: float
    category: str
    description: Optional[str]
    expense_date: date
    created_at: datetime
    is_recurring: bool
    user_id: int


class TotalResponse(BaseModel):
    total: float
    count: int
