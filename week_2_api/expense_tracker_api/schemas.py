from pydantic import BaseModel,Field
from typing import Optional


class ExpenseRequest(BaseModel):

    title: str = Field(
        min_length=2,
        max_length=50
    )

    price: float = Field(
        gt=0
    )

    category: str = Field(
        min_length=2,
        max_length=30
    )

class ExpenseResponse(BaseModel):

    id: int
    title: str
    price: float
    category: str

class ExpenseUpdate(BaseModel):

    title: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50
    )

    price: Optional[float] = Field(
        default=None,
        gt=0
    )

    category: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=30
    )

class TotalResponse(BaseModel):

    total: float